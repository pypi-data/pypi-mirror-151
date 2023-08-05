import os.path

from abc import ABC, abstractmethod
import uuid
import logging

logger = logging.getLogger("download_manager")


class Writer(ABC):
    '''
    The Writer class is dedicated to perform parallel write into designations.
    According to the sub-implementation writing shall manage concurrence
    writting access.
    '''

    @abstractmethod
    def write(self, chunk: bytes, offset: int):
        """
        Write element into tue current place
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        '''
            Close the writer and finalize action once the entire dataset is
            transferred.
        '''
        raise NotImplementedError


class FileWriter(Writer):
    def __init__(self, out_path: str, file_size: int, retry=False):
        self.out_file = os.path.realpath(out_path + '.' +
                                         str(uuid.uuid4()))
        self.final_filename = out_path
        self.file_size = file_size
        self.retry = retry

    def _init_writer(self):
        if self.retry:
            self.out_file = self.final_filename
        if not os.path.exists(self.out_file):
            logger.debug(f"initializing {self.out_file}")
            # Prepare the file with its final size
            with open(self.out_file, "wb") as fp:
                fp.seek(self.file_size - 1)
                fp.write(b'\0')

    def write(self, chunk: bytes, offset: int):
        self._init_writer()
        with open(self.out_file, "r+b") as fp:
            fp.seek(offset)
            fp.write(chunk)

    def close(self):
        if os.path.exists(self.out_file):
            logger.debug(f'Move to file {self.final_filename}')
            os.rename(self.out_file, self.final_filename)
