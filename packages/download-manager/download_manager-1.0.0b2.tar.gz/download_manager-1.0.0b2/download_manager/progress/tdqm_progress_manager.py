from .progress_manager import ProgressManager
from tqdm import tqdm
from logging import Handler, NOTSET


class TdqmProgressManager(ProgressManager):
    def __init__(self, name: str, total: int, **kwargs):
        self._tqdm = tqdm(desc=name, total=total, **kwargs)

    @property
    def total(self):
        return self._tqdm.total

    @property
    def cursor(self):
        return self._tqdm.pos

    def update(self, count: int = 1):
        self._tqdm.update(count)


class TqdmLoggingHandler(Handler):
    """
    This class is used to manage the logging with the progress bar.
    """
    def __init__(self, level=NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)
