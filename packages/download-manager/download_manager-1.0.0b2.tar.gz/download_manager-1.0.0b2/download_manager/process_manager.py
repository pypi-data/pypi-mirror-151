import logging
from concurrent.futures import ProcessPoolExecutor

logger = logging.getLogger("process_manager")


class ManagedProcessExecutor(ProcessPoolExecutor):
    """
    Managed Thread Pool Executor. A subclass of ProcessPoolExecutor.
    """

    def __init__(self, max_workers, storage_limit_size, output_folder):
        ProcessPoolExecutor.__init__(self, max_workers=max_workers)
        self._futures = []
        self._excepts = []

    def submit(self, fn, *args, **kwargs):
        future = super().submit(fn, *args, **kwargs)
        self._futures.append(future)
        return future

    def done(self):
        self._update()
        return len(self._futures) == 0

    def get_exceptions(self):
        return self._excepts

    def _update(self):
        for x in self._futures:
            if x.done():
                if x.exception():
                    self._excepts.append(x.exception())
                    logger.error(x.exception())
                else:
                    name, start, end, writer = x.result()
                    logger.info(f'Chunk Downloaded {name} [{start}, {end}]')
                self._futures.remove(x)
