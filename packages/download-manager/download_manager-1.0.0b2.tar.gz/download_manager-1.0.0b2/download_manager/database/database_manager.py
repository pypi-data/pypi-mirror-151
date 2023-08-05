from download_manager.database.database_objects import WorkingData, Chunk
from download_manager.database.database_objects import CompletedHistory
from download_manager.database.database_objects import db as database
from datetime import datetime
from peewee import SqliteDatabase
from enum import Enum
import functools
import os
import logging

logger = logging.getLogger("download_manager")


class DatabaseManagerException (Exception):
    pass


class Status (Enum):
    UNKNOWN = 'UNKNOWN'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


def database_chunk_handling(func):
    @functools.wraps(func)
    def wrapper_chunk_download(*args, **kwargs):
        filename = kwargs.get('filename')
        start = kwargs.get('start')
        stop = kwargs.get('stop')

        data = DatabaseManager.get_working_data(filename)
        DatabaseManager.set_status(data=data, start=start, end=stop,
                                   status=Status.STARTED)
        try:
            value = func(*args, **kwargs)  # process transfer
        except Exception as e:
            DatabaseManager.set_status(data=data, start=start, end=stop,
                                       status=Status.ERROR)
            raise e

        DatabaseManager.set_status(data=data, start=start, end=stop,
                                   status=Status.COMPLETED)
        # Checks if file finished
        try:
            DatabaseManager.finish_download(data)
            logger.info(f"File {filename} Downloaded.")
        except DatabaseManagerException:
            # Case of chunks still to be downloaded.
            pass
        return value
    return wrapper_chunk_download


class DatabaseManager:
    initialized = False
    DB_FILE = 'download_manager.db'

    '''
    DatabaseManager gathes all the method required to manage database update
    while data downlaod:
     1- identify product to download
     2- defines chunks list for this product
     3- manages chunks status update during products transfers
     4- manages end of download with removing product in progress and
        recoding history
    '''
    @staticmethod
    def create(database_path: str = None):
        # About pragma : to manage CASCADE on_delete
        # see https://docs.peewee-orm.com/en/latest/peewee/relationships.html
        if not DatabaseManager.initialized:
            path = DatabaseManager._init_database_path(database_path)
            database.initialize(SqliteDatabase(
                path, pragmas={'foreign_keys': 1}))
            if not WorkingData.table_exists():
                WorkingData.create_table()
            if not Chunk.table_exists():
                Chunk.create_table()
            if not CompletedHistory.table_exists():
                CompletedHistory.create_table()
            DatabaseManager.initialized = True

    @staticmethod
    def _init_database_path(folder: str):
        # Case of memory
        if folder == ':memory:':
            return folder
        # Default
        if folder is None:
            folder = os.path.join(os.environ.get('HOME', '.'), ".dm")
        # User defined
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        db = os.path.join(folder, DatabaseManager.DB_FILE)
        if not os.path.exists(db):
            open(db, 'w').close()

        return db

    @staticmethod
    def exists_working_data(filename):
        return WorkingData.select().where(
            WorkingData.name == filename).exists()

    @staticmethod
    def add_working_data(name: str, size: int, date: datetime) -> WorkingData:
        return WorkingData.create(name=name, size=size, date=date)

    @staticmethod
    def get_working_data(name: str) -> WorkingData:
        if DatabaseManager.exists_working_data(name):
            query = WorkingData.select().where(WorkingData.name == name)
            return query[0]
        raise DatabaseManagerException(f"Working data {name} not found.")

    @staticmethod
    def remove_working_data(name: str) -> int:
        return DatabaseManager.get_working_data(name).delete()

    @staticmethod
    def list_working_data() -> list:
        return WorkingData

    @staticmethod
    def clean_all_working_data() -> int:
        return WorkingData.delete().execute()

    @staticmethod
    def add_chunk(data, start, end) -> WorkingData:
        return Chunk.create(data=data, start=start, end=end,
                            status=Status.UNKNOWN.value)

    @staticmethod
    def get_chunk(data: WorkingData, start: int, end: int) -> Chunk:
        query = Chunk.select().where((Chunk.data == data) &
                                     (Chunk.start == start) &
                                     (Chunk.end == end))
        if query.exists():
            return query[0]
        raise DatabaseManagerException(
            f"Chunk {data.name}/[{start},{end}] not found")

    @staticmethod
    def get_chunk_id(key: int) -> Chunk:
        query = Chunk.select().where(Chunk.id == key)

        if query.exists():
            return query.execute()
        raise DatabaseManagerException(
            f"Chunk {key} not found")

    @staticmethod
    def remove_chunk(data, start=None, end=None) -> int:
        return DatabaseManager.get_chunk(data, start, end).delete_instance()

    @staticmethod
    def list_chunk() -> list:
        return Chunk

    @staticmethod
    def clean_all_chunk() -> int:
        return Chunk.delete().execute()

    @staticmethod
    def check_completion(data: WorkingData) -> bool:
        return Chunk.select().where(
            (Chunk.data == data) &
            (Chunk.status != Status.COMPLETED)).count() == 0

    @staticmethod
    def set_status(data, start, end, status: Status):
        query = Chunk.update(status=status).where(
            (Chunk.data == data) & (Chunk.start == start) & (Chunk.end == end))
        return query.execute()

    @staticmethod
    def finish_download(data: WorkingData):
        if DatabaseManager.check_completion(data):
            CompletedHistory.create(name=data.name, size=data.size)
            query = Chunk.delete().where(Chunk.data == data)
            query.execute()
            data.delete_instance()
        else:
            raise DatabaseManagerException("Download not completed.")

    @staticmethod
    def is_download_finished(filename: str):
        if DatabaseManager.exists_working_data(filename):
            data = DatabaseManager.get_working_data(filename)
            return DatabaseManager.check_completion(data)
        return True

    @staticmethod
    def is_download_started(filename: str):
        if DatabaseManager.exists_working_data(filename):
            return DatabaseManager.get_working_data_with_unknown().where(
                    WorkingData.name == filename).exists() and \
                not DatabaseManager.get_working_data_with_pending().where(
                    WorkingData.name == filename).exists() and \
                not DatabaseManager.get_working_data_with_error().where(
                    WorkingData.name == filename).exists() and \
                not DatabaseManager.get_working_data_with_completed().where(
                    WorkingData.name == filename).exists()
        return True

    @staticmethod
    def list_completed_history() -> list:
        return CompletedHistory

    @staticmethod
    def clean_all_completed_history() -> int:
        return CompletedHistory.delete().execute()

    @staticmethod
    def get_working_data_with_error():
        return WorkingData.select().\
            join(Chunk, on=((Chunk.data == WorkingData.id) &
                            (Chunk.status == Status.ERROR))). \
            group_by(WorkingData.name)

    @staticmethod
    def get_working_data_with_unknown():
        return WorkingData.select(). \
            join(Chunk, on=((Chunk.data == WorkingData.id) &
                            (Chunk.status == Status.UNKNOWN))).\
            group_by(WorkingData.name)

    @staticmethod
    def get_working_data_with_pending():
        return WorkingData.select().join(
            Chunk, on=((Chunk.data == WorkingData.id) &
                       (Chunk.status == Status.STARTED)))

    @staticmethod
    def get_working_data_with_completed():
        return WorkingData.select().join(
            Chunk, on=((Chunk.data == WorkingData.id) &
                       (Chunk.status == Status.COMPLETED)))

    @staticmethod
    def print_working():
        import logging
        logger = logging.getLogger("print_database")
        logger.setLevel(logging.INFO)

        logger.info("Downloading datasets:")
        for data in DatabaseManager.list_working_data():
            logger.info(f"- {data.name} - {data.size} - {data.date}:")
            for chunk in Chunk.select().where(Chunk.data == data):
                logger.info(f"   [{chunk.start},{chunk.end}]: {chunk.status}:")
        logger.info("Download history")
        for completed in DatabaseManager.list_completed_history():
            logger.info(f"   - {completed.timestamp}: {completed.name}: "
                        f"{completed.size} - {completed.checksum}")
