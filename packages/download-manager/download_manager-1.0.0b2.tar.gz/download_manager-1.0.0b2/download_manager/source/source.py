import time
from abc import ABC, abstractmethod
from drb import DrbNode
from drb.exceptions import DrbException
from drb_impl_odata import ODataQueryPredicate
from drb_impl_odata.exceptions import OdataRequestException
from requests.auth import AuthBase
from typing import List
from drb_impl_odata.odata_nodes import ODataServiceNode, OdataServiceType

from download_manager.utility import parse_csv


class ODataDownloadRequestException(Exception):
    pass


class Source(ABC):
    @abstractmethod
    def list(self, filter: str, order: str, top: int,
             skip: int, names: str, date) -> List[DrbNode]:
        """The abstract method aims to return the list of DRB Node retrieved
        from the service.

        :param filter: data filter in the service filter systel syntax.
        :param top: number of element to return.
        :param skip: number of element to skip.
        :return: the generator of retrieved nodes
        """
        raise NotImplementedError

    @abstractmethod
    def content_size(self, node: DrbNode) -> int:
        '''
        Use service to retrieve node size.
        :param node: the node to retrieve the content size
        :return: the size of the content.
        '''
        raise NotImplementedError

    @abstractmethod
    def content_checksum(self, node: DrbNode) -> str:
        '''
        Use service to retrieve node content checksum (default is MD5)
        :param node: node use to get content checksum
        :return: the MD5 checksum
        '''
        raise NotImplementedError

    @abstractmethod
    def publication_date(self, node: DrbNode) -> str:
        '''
        Use service to retrieve node publication date
        :param node:
        :return:
        '''
        raise NotImplementedError


def _join_with_none(sep: str, join_list: List[str]):
    """
    Manage join string canceling None element strings:
      ' and '.join(['A','B'])
      return 'A and B'

      ' and '.join(['A','B', None])
      return 'A and B'

      ' and '.join(['A', None])
      return 'A'

    :param sep:
    :param join_list:
    :return:
    """
    lst = [x for x in join_list if x is not None]
    return sep.join(lst)


class OdataSource(Source):
    """
    ODataSource Class is the implementation of DrbNode retrieval from an OData
    service.
    """

    def __init__(self, service: str, auth: AuthBase = None):
        self.service = service
        self.auth = auth
        self.odata_service = ODataServiceNode(self.service, auth=self.auth)

    def list(self, filter: str = None, order=None, top: int = None,
             skip: int = None, names: str = None, date=None) -> List[DrbNode]:
        _type = self.odata_service.type_service
        online_filter = None
        name_filter = None
        date_filter = None
        if _type == OdataServiceType.DHUS:
            if filter is None or 'Online' not in filter:
                online_filter = 'Online eq true'
            if names is not None:
                products = parse_csv(names)
                filt = []
                for name in products:
                    filt.append(f"Name eq '{name}'")
                name_filter = _join_with_none(' or ', filt)
            if date is not None:
                _and = f'{filter} and ' if filter is not None else ''
                date_filter = f'{_and}IngestionDate gt {date}'
                order = f'IngestionDate {order}'

        if _type == OdataServiceType.ONDA_DIAS:
            if filter is None or 'offline' not in filter:
                online_filter = 'offline eq false'
            if names is not None:
                products = parse_csv(names)
                filt = []
                for name in products:
                    filt.append(f"name eq '{name}'")
                name_filter = _join_with_none(' or ', filt)
            if date is not None:
                _and = f'{filter} and ' if filter is not None else ''
                date_filter = f'{_and}creationDate gt {date}'
                order = f'creationDate {order}'

        if _type == OdataServiceType.CSC:
            if filter is None or 'Online' not in filter:
                online_filter = 'Online eq true'
            if names is not None:
                products = parse_csv(names)
                filt = []
                for name in products:
                    filt.append(f"Name eq '{name}'")
                name_filter = _join_with_none(' or ', filt)
            if date is not None:
                _and = f'{filter} and ' if filter is not None else ''
                date_filter = f'{_and}PublicationDate gt {date}'
                order = f'PublicationDate {order}'

        if online_filter is not None:
            filters = _join_with_none(' and ', [filter, online_filter])
        if name_filter is not None:
            filters = _join_with_none(' and ', [filters, name_filter])
        if date_filter is not None:
            filters = _join_with_none(' and ', [filters, date_filter])
        else:
            filters = filter
        try:
            nodes = self.odata_service[
                ODataQueryPredicate(
                    filter=None, order=None, top=None, skip=None)]
        except DrbException:
            return []
        if names is not None:
            return nodes
        if skip is None or skip == 0:
            return nodes[:top]
        new_top = skip + top
        try:
            return nodes[skip:new_top]
        except OdataRequestException:
            time.sleep(5)
            return nodes[skip:new_top]

    def content_size(self, node: DrbNode) -> int:
        content_size = 0
        _type = self.odata_service.type_service
        if _type == OdataServiceType.DHUS:
            content_size = node.get_attribute('ContentLength')
        if _type == OdataServiceType.ONDA_DIAS:
            content_size = node.get_attribute('size')
        if _type == OdataServiceType.CSC:
            content_size = node.get_attribute('ContentLength')
        return content_size

    def content_checksum(self, node: DrbNode) -> str:
        content_checksum = None
        _type = self.odata_service.type_service
        if _type in (OdataServiceType.DHUS, OdataServiceType.CSC):
            content_checksum = node.get_attribute('Checksum')[0]['Value']
        return content_checksum

    def publication_date(self, node: DrbNode) -> str:
        content_size = 0
        _type = self.odata_service.type_service
        if _type == OdataServiceType.DHUS:
            content_size = node.get_attribute('CreationDate')
        if _type == OdataServiceType.CSC:
            content_size = node.get_attribute('PublicationDate')
        if _type == OdataServiceType.ONDA_DIAS:
            raise NotImplementedError()
        return content_size
