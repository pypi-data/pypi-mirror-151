import datetime
import logging
import io
import time

from requests.auth import AuthBase

from download_manager.utility import slice_file
from download_manager.storage.storage_manager import StorageManager
from download_manager.storage.storage_manager import storage_chunk_handling
from download_manager.destination.writer import FileWriter
from download_manager.database.database_manager import database_chunk_handling
from download_manager.database.database_manager import DatabaseManager
from download_manager.progress.progress_factory import progress_chunk_handling
from download_manager.process_manager import ManagedProcessExecutor
from download_manager.source.source_factory import SourceFactory, Source
from drb import DrbNode

logger = logging.getLogger("download_manager")


class DatabaseManagerException(Exception):
    pass


@progress_chunk_handling
@storage_chunk_handling
@database_chunk_handling
def handler(node: DrbNode, start: int, stop: int, filename: str,
            writer: FileWriter, **kwargs):
    '''
    Handler dedicated to downlaod chunks
    :param node:
    :param start:
    :param stop:
    :param filename:
    :param writer:
    :param checksum:
    :return:
    '''
    buff = node.get_impl(io.BytesIO, start=start, end=stop - start).read()
    # open the file and write the content of the download
    writer.write(buff, start)
    return filename, start, stop, writer


class DownloadManager:
    """
    TODO:
    Download manager class is the entry point class for download manager
    cli. The first objective of this class is to handle download commands and
    their configurations. DownloadManager class is also here to manage
    download pools, start/stop pools per services, submit new downloads,
    manage the priority between download.

    Also the download manager aims to handle a basic storage with a controlled
    limit of size. Then an eviction mechanism shall be implemented.

    persistence: it could be possible to save Download manager configuration
    and services, keep persistent the current downloads after stopping DM
    and resume them.
    """

    def __init__(self, service: str, auth: AuthBase = None,
                 database_folder: str = None, output_folder: str = '.',
                 process_number: int = 2, chunk_size: int = 4194304,
                 quiet=True, storage_limit_size=None,
                 verify=False, resume=False):
        self._service = service
        self._auth = auth
        self._database_folder = database_folder
        self._bars = {}
        self._output_folder = output_folder
        self._executor: ManagedProcessExecutor = None
        self._process_number = process_number
        self._chunk_size = chunk_size
        self._quiet = quiet
        self._storage_limit_size = storage_limit_size
        self._storage_manager = StorageManager(folder=output_folder,
                                               size_limit=storage_limit_size)
        self._resume = resume
        self._verify = verify

    @property
    def source(self):
        return SourceFactory.create_source(self._service, self._auth)

    @property
    def storage_manager(self):
        return self._storage_manager

    @staticmethod
    def find_nodes(source: Source, filter: str, order: str = None,
                   limit: int = 10, skip: int = 0, bulk: list = None,
                   date=None
                   ):
        """
            Return a List of DrbNodes to be downloaded.

            Parameters:
                source: (Source) the source to request.
                filter: (str) filter apply to query products.
                order: (str) Order the result of the request.
                limit: (int) ODate query top
                skip: (int) How many product to skip
                bulk: (str) Path to a csv file

            Return:
                A list of OdataProductNode.
            """
        return source.list(
            filter=filter,
            order=order,
            top=limit,
            skip=skip,
            names=bulk,
            date=date
        )

    def start(self):
        DatabaseManager.create(self._database_folder)

        pendings = DatabaseManager.get_working_data_with_pending()
        unknowns = DatabaseManager.get_working_data_with_unknown()
        errors = DatabaseManager.get_working_data_with_error()

        unfinished_list = [uf.name for uf in pendings + errors + unknowns]

        # Currently just raise a warn
        # TBC: check possible actions with StorageManagement
        # Current issue is database does not contains any sources info:
        #    the user shall restart the transfer itself.
        if len(unfinished_list) > 0:
            logger.warning(f"Previous run interrupted for data "
                           f"{', '.join(unfinished_list)}")

        if self._executor is None:
            self._executor = ManagedProcessExecutor(
                max_workers=self._process_number,
                storage_limit_size=self._storage_limit_size,
                output_folder=self._output_folder)

    def stop(self):
        if self._executor is not None:
            self._executor.shutdown(wait=True)
        self._executor = None

    def submit(self, node: DrbNode, checksum: bool = None):
        verify_checksum = self._verify if checksum is None else checksum
        # Add Working data database entry
        file_size = self.source.content_size(node)
        name = node.name

        # Checks if node is already downloading
        if DatabaseManager.exists_working_data(name):
            if not self._resume:
                raise DatabaseManagerException(
                    f"Product {node.name} already managed "
                    f"(use force to bypass)")

        self._storage_manager.check_and_clean_folder(
            file_size, DatabaseManager.list_completed_history())

        wd = DatabaseManager.add_working_data(
            name=node.name, size=file_size, date=datetime.datetime.now())

        # prepare writer
        writer = FileWriter(
            out_path=self._storage_manager.path_in_store(node.name),
            file_size=file_size)

        # prepare chunk list
        chunks = slice_file(file_size, self._chunk_size)
        for chunk in chunks:
            DatabaseManager.add_chunk(wd, chunk.start, chunk.end)

        # checksum
        if verify_checksum:
            content_checksum = self.source.content_checksum(node)
        else:
            content_checksum = None

        for chunk in chunks:
            self._executor.submit(
                handler, node=node, start=chunk.start, stop=chunk.end,
                filename=node.name, writer=writer, checksum=content_checksum,
                storage_manager=self._storage_manager, size=file_size,
                quiet=self._quiet
            )

    def join(self):
        while not self._executor.done():
            time.sleep(1)
