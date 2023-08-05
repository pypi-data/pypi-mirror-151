import hashlib
import os
import functools
import logging

from download_manager.database.database_manager import DatabaseManager

logger = logging.getLogger("download_manager")


class StorageManagerException(Exception):
    pass


class StorageManagerWrongChecksumException(Exception):
    pass


def storage_chunk_handling(func):
    @functools.wraps(func)
    def wrapper_chunk_download(*args, **kwargs):
        filename = kwargs.get('filename')
        checksum = kwargs.get('checksum')
        writer = kwargs.get('writer')
        sm = kwargs.get('storage_manager')

        try:
            value = func(*args, **kwargs)  # process transfer
        except Exception as e:
            raise e

        if DatabaseManager.is_download_finished(filename):
            # logger.info(f"Closing file {filename}")
            writer.close()
            if checksum is not None:
                md5 = sm.compute_md5(sm.path_in_store(filename))
                # logger.info(f"Compute MD5 for {filename}: "
                #             f"computed={md5}/reference={checksum}")
                if md5 != checksum:
                    raise StorageManagerWrongChecksumException(
                        f"{filename}: computed={md5}, expected={checksum}")

        return value

    return wrapper_chunk_download


def file_as_bytes(file):
    with file:
        return file.read()


class StorageManager:
    def __init__(self, folder: str, size_limit: int = None):
        self._folder = self._init_storage_path(folder)
        self._size_limit = size_limit

    @staticmethod
    def _init_storage_path(folder: str):
        # Default
        if folder is None or folder == '':
            folder = os.path.join(os.environ.get('HOME', '.'), ".dm", "data")
        # User defined
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        return folder

    def path_in_store(self, filename):
        return os.path.join(self._folder, filename)

    @staticmethod
    def compute_md5(file) -> str:
        return hashlib.md5(file_as_bytes(open(file, 'rb'))).hexdigest()

    @staticmethod
    def get_storage_size(folder) -> int:
        size = 0
        for path, dirs, files in os.walk(folder):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)
        return size

    def check_and_clean_folder(self, size_to_add: int = 0,
                               completed_data=None):
        if self._size_limit is None:
            return
        while True:
            # Compute the folder size
            current_folder_size = StorageManager.get_storage_size(self._folder)
            future_size = current_folder_size + size_to_add
            # checks the folder limits to exist the loop
            if future_size < self._size_limit:
                break
            # if size limit exceeded: remote still existing data from db.
            if completed_data is not None:
                for data in completed_data:
                    data_to_delete = os.path.join(self._folder, data.name)
                    if os.path.exists(data_to_delete):
                        logger.warning(
                            f"Storage full: removing {data_to_delete}"
                        )
                        os.remove(data_to_delete)
                        break

            raise StorageManagerException(
                f"Storage limit reached ({self._size_limit}). The folder "
                f"{self._folder} size is {future_size} with unknown "
                f"data: Please cleanup manually")

    def exists_finished_data(self, filename):
        return os.path.exists(os.path.join(self._folder, filename))

    def exists_running_data(self, filename):
        # running data are encoded with filename.xxxxxx
        return len([x for x in os.listdir(self._folder)
                    if x.startswith(filename)]) > 0
