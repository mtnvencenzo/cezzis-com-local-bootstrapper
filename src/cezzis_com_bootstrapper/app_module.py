from injector import Binder, Injector, Module, noscope, singleton
from mediatr import Mediator

from cezzis_com_bootstrapper.application.concerns.messaging.commands.create_kafka_command import (
    CreateKafkaCommandHandler,
)
from cezzis_com_bootstrapper.application.concerns.storage.commands.create_blobstorage_command import (
    CreateBlobstorageCommandHandler,
)
from cezzis_com_bootstrapper.domain.config.azure_storage_options import AzureStorageOptions, get_azure_storage_options
from cezzis_com_bootstrapper.domain.config.kafka_options import KafkaOptions, get_kafka_options
from cezzis_com_bootstrapper.infrastructure.services.azure_blob_service import AzureBlobService
from cezzis_com_bootstrapper.infrastructure.services.iazure_blob_service import IAzureBlobService
from cezzis_com_bootstrapper.infrastructure.services.ikafka_service import IKafkaService
from cezzis_com_bootstrapper.infrastructure.services.kafka_service import KafkaService


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
        # For azure blob storage setup
        binder.bind(AzureStorageOptions, get_azure_storage_options(), scope=singleton)
        binder.bind(IAzureBlobService, AzureBlobService, scope=singleton)
        binder.bind(CreateBlobstorageCommandHandler, CreateBlobstorageCommandHandler, scope=noscope)
        # for kafka setup
        binder.bind(KafkaOptions, get_kafka_options(), scope=singleton)
        binder.bind(IKafkaService, KafkaService, scope=singleton)
        binder.bind(CreateKafkaCommandHandler, CreateKafkaCommandHandler, scope=noscope)


injector = create_injector()
