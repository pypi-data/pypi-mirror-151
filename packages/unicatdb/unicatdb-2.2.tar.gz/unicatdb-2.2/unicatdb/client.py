from .openapi_client import FindingsApi, ApiClient, ChartsApi, AttachmentsApi, SchemasApi, TenantsApi, ExportApi
from . import Configuration
from tusclient import client


class Client():

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()

        self.__configuration = configuration
        self.__configured_api_client = ApiClient(configuration)

    # support for with() statement
    def __enter__(self):
        self.__configured_api_client.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__configured_api_client.__exit__(exc_type, exc_value, traceback)

    def close(self):
        self.__configured_api_client.close()

    # individual APIs as configured properties:

    @property
    def attachments(self):
        return AttachmentsApi(self.__configured_api_client)

    @property
    def charts(self):
        return ChartsApi(self.__configured_api_client)

    @property
    def export(self):
        return ExportApi(self.__configured_api_client)

    @property
    def findings(self):
        return FindingsApi(self.__configured_api_client)

    @property
    def schemas(self):
        return SchemasApi(self.__configured_api_client)

    @property
    def tenants(self):
        return TenantsApi(self.__configured_api_client)

    def get_tus_client_for_finding(self, tenant_id: str, finding_id: str) -> client.TusClient:
        url = self.__configuration.host + f"/{tenant_id}/findings/{finding_id}/attachments/tus"
        return client.TusClient(url, headers={'Authorization': f"Bearer {self.__configuration.access_token}"})
