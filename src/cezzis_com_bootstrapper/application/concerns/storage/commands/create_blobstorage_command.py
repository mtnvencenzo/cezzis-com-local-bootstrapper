from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.domain.config.azure_storage_options import AzureStorageOptions
from cezzis_com_bootstrapper.infrastructure.services.iazure_blob_service import IAzureBlobService


class CreateBlobStorageCommand(GenericQuery[bool]):
    """"""

    pass


@Mediator.handler
class CreateBlobstorageCommandHandler:
    @inject
    def __init__(self, azure_blob_service: IAzureBlobService, azure_storage_options: AzureStorageOptions):
        self.azure_blob_service = azure_blob_service
        self.azure_storage_options = azure_storage_options

    async def handle(self, request: CreateBlobStorageCommand) -> bool:
        await self.azure_blob_service.create_container(self.azure_storage_options.account_avatars_container_name)
        return True
