from injector import Binder, Module, singleton
from mediatr import Mediator

from cezzis_com_bootstrapper.application.concerns.storage.commands.create_container_command import (
    CreateContainerCommandHandler,
)
from cezzis_com_bootstrapper.domain.config.azure_storage_options import AzureStorageOptions, get_azure_storage_options
from cezzis_com_bootstrapper.infrastructure.services.azure_blob_service import AzureBlobService
from cezzis_com_bootstrapper.infrastructure.services.iazure_blob_service import IAzureBlobService


class AppModule(Module):
    def configure(self, binder: Binder):
        binder.bind(Mediator, Mediator, scope=singleton)
        binder.bind(AzureStorageOptions, get_azure_storage_options(), scope=singleton)
        binder.bind(IAzureBlobService, AzureBlobService, scope=singleton)
        binder.bind(CreateContainerCommandHandler, CreateContainerCommandHandler, scope=singleton)
