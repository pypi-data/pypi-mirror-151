from abc import ABC, abstractmethod

import download_manager.source.source
from download_manager.download_manager import DownloadManager
from drb_impl_odata import ODataQueryPredicate
import logging

logger = logging.getLogger("download_manager")


class Trigger(ABC):
    @abstractmethod
    def run(self, filter: str, **kwargs):
        '''
        Managed expected actions to handle the trigger.
        :return:
        '''
        raise NotImplementedError


class ContinuousTrigger(Trigger):
    def __init__(self, download_manager: DownloadManager):
        self._download_manager = download_manager
        self._current_date = None

    def run(self, filter: str, **kwargs):
        while True:
            nodes = self._download_manager.find_nodes(
                source=self._download_manager.source,
                filter=filter,
                order='asc',
                limit=1,
                date=self._current_date)
            for node in nodes:
                # Checks if product is already present
                if self._download_manager.storage_manager. \
                        exists_running_data(node.name):
                    logger.info(f"{node.name} already loaded.")
                    continue

                try:
                    self._download_manager.submit(node)
                except Exception as e:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.error(f"Error while submitting {node.name}", e)
                    else:
                        logger.error(
                            f"Error while submitting {node.name}: {str(e)}")

                self._current_date = \
                    self._download_manager.source.publication_date(node)
            self._download_manager.join()
