from abc import ABC, abstractmethod
from download_manager.progress.event import EventManager


class ProgressManager(ABC):
    @abstractmethod
    def update(self, count: int = 1):
        raise NotImplementedError()


class BasicProgressManager(ProgressManager):
    def __init__(self, total: int, current: int = 0):
        self._total = total
        self._current = current
        self.change = EventManager()

    @property
    def total(self):
        return self._total

    @property
    def cursor(self):
        return self._current

    def update(self, count: int = 1):
        self._current += count
        self.change.notify(self, 'progress', action='inc', increment=count)
        if self._current >= self._total:
            self.change.notify(self, 'progress', action='end')
