from injector import Binder, Injector, Module, Scope, noscope, singleton, threadlocal
from mediatr import Mediator

from cezzis_com_bootstrapper.application.concerns.storage.commands.create_containers_command import (
    CreateContainersCommandHandler,
)
from cezzis_com_bootstrapper.domain.config.azure_storage_options import AzureStorageOptions, get_azure_storage_options
from cezzis_com_bootstrapper.infrastructure.services.azure_blob_service import AzureBlobService
from cezzis_com_bootstrapper.infrastructure.services.iazure_blob_service import IAzureBlobService


def create_injector() -> Injector:
    return Injector([AppModule()])

def my_class_handler_manager(handler_class, is_behavior=False):
    if is_behavior:
        # custom logic
        pass

    return injector.get(handler_class)


class AppModule(Module):
    def configure(self, binder: Binder):
        binder.bind(Mediator, Mediator(handler_class_manager=my_class_handler_manager), scope=singleton)
        binder.bind(AzureStorageOptions, get_azure_storage_options(), scope=singleton)
        binder.bind(IAzureBlobService, AzureBlobService, scope=singleton)
        binder.bind(CreateContainersCommandHandler, CreateContainersCommandHandler, scope=noscope)




injector = create_injector()

