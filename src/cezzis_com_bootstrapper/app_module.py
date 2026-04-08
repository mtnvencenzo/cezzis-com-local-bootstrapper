from injector import Binder, Injector, Module, noscope, singleton
from mediatr import Mediator

from cezzis_com_bootstrapper.application.concerns import (
    CreateBlobStorageCommandHandler,
    CreateKafkaCommandHandler,
    CreateRabbitMqCommandHandler,
)
from cezzis_com_bootstrapper.domain.config import (
    AzureStorageOptions,
    BootstrapperOptions,
    KafkaOptions,
    RabbitMqOptions,
    get_azure_storage_options,
    get_bootstrapper_options,
    get_kafka_options,
    get_rabbitmq_options,
)
from cezzis_com_bootstrapper.infrastructure.services import (
    AzureBlobService,
    IAzureBlobService,
    IKafkaService,
    IRabbitMqAdminService,
    KafkaService,
    RabbitMqAdminService,
)


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
        # Bootstrapper feature flags
        bootstrapper_options = get_bootstrapper_options()
        binder.bind(BootstrapperOptions, bootstrapper_options, scope=singleton)
        # For azure blob storage setup
        if bootstrapper_options.enable_blob_storage:
            binder.bind(AzureStorageOptions, get_azure_storage_options(), scope=singleton)
            binder.bind(IAzureBlobService, AzureBlobService, scope=singleton)
            binder.bind(CreateBlobStorageCommandHandler, CreateBlobStorageCommandHandler, scope=noscope)
        # for kafka setup
        if bootstrapper_options.enable_kafka:
            binder.bind(KafkaOptions, get_kafka_options(), scope=singleton)
            binder.bind(IKafkaService, KafkaService, scope=singleton)
            binder.bind(CreateKafkaCommandHandler, CreateKafkaCommandHandler, scope=noscope)
        # For RabbitMQ Setup
        if bootstrapper_options.enable_rabbitmq:
            binder.bind(RabbitMqOptions, get_rabbitmq_options(), scope=singleton)
            binder.bind(IRabbitMqAdminService, RabbitMqAdminService, scope=singleton)
            binder.bind(CreateRabbitMqCommandHandler, CreateRabbitMqCommandHandler, scope=noscope)


injector = create_injector()
