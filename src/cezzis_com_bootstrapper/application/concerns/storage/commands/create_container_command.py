from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.infrastructure.services.iazure_blob_service import IAzureBlobService


class CreateContainerCommand(GenericQuery[bool]):
    def __init__(self, container_name: str):
        self.container_name = container_name


@Mediator.handler
class CreateContainerCommandHandler:
    @inject
    def __init__(self, azure_blob_service: IAzureBlobService):
        self.azure_blob_service = azure_blob_service

    async def handle(self, request: CreateContainerCommand) -> bool:
        await self.azure_blob_service.create_container(request.container_name)
        return True
