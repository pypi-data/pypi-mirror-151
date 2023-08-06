from . import openapi_client
from .servers import Servers


class Configuration(openapi_client.Configuration):

    def __init__(self, access_token=None, server: Servers = Servers.UNICATDB_ORG):
        self.access_token = access_token
        super().__init__(host=server.value)
