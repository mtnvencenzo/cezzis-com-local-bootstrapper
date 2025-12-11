import logging

from azure.storage.blob import BlobServiceClient, PublicAccess
from injector import inject

from cezzis_com_bootstrapper.domain import AzureStorageOptions
from cezzis_com_bootstrapper.infrastructure.services.iazure_blob_service import IAzureBlobService


class AzureBlobService(IAzureBlobService):
    """Azure Blob Storage service implementation."""

    @inject
    def __init__(self, azure_storage_options: AzureStorageOptions):
        self._connection_string = azure_storage_options.connection_string
        self._container_name = azure_storage_options.account_avatars_container_name
        self.logger = logging.getLogger("azure_blob_service")

    async def create_container(self, container_name: str) -> None:
        """Create a container in Azure Blob Storage.

        Args:
            container_name (str): The name of the container to create.
        """

        blob_service_client = BlobServiceClient.from_connection_string(self._connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        try:
            if not container_client.exists():
                container_client.create_container(public_access=PublicAccess.CONTAINER)
                self.logger.info(f"Container '{container_name}' created successfully.")
            else:
                container_client.set_container_access_policy(
                    signed_identifiers={}, public_access=PublicAccess.CONTAINER
                )
                self.logger.info(f"Container '{container_name}' already exists. Access policy updated to public.")
        except Exception as e:
            self.logger.exception(f"Failed to create or update container '{container_name}'", extra={"error": str(e)})
            raise
        finally:
            pass
