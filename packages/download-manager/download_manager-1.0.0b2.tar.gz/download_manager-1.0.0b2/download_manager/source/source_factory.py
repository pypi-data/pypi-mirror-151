from requests.auth import AuthBase
from download_manager.source.source import OdataSource, Source


class SourceFactory:
    @staticmethod
    def create_source(service: str, auth: AuthBase) -> Source:
        """
        Current implementation only manage OData - Next shall use drb resolver.
        :param service:
        :param auth:
        :return:
        """
        return OdataSource(service=service, auth=auth)
