from injector import Binder, Injector, Module, noscope, singleton
from mediatr import Mediator

from cezzis_com_bootstrapper.application.concerns import (
    CreateBlobStorageCommandHandler,
    CreateCosmosDbCommandHandler,
    CreateKafkaCommandHandler,
    CreateQdrantCommandHandler,
    CreateRabbitMqCommandHandler,
)
from cezzis_com_bootstrapper.domain.config import (
    AzureStorageOptions,
    CosmosDbOptions,
    KafkaOptions,
    RabbitMqOptions,
    get_azure_storage_options,
    get_cosmosdb_options,
    get_kafka_options,
    get_rabbitmq_options,
)
from cezzis_com_bootstrapper.domain.config.qdrant_options import QdrantOptions, get_qdrant_options
from cezzis_com_bootstrapper.infrastructure.services import (
    AzureBlobService,
    CosmosDbService,
    IAzureBlobService,
    ICosmosDbService,
    IKafkaService,
    IQdrantService,
    IRabbitMqAdminService,
    KafkaService,
    QdrantService,
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
        # For azure blob storage setup
        binder.bind(AzureStorageOptions, get_azure_storage_options(), scope=singleton)
        binder.bind(IAzureBlobService, AzureBlobService, scope=singleton)
        binder.bind(CreateBlobStorageCommandHandler, CreateBlobStorageCommandHandler, scope=noscope)
        # for kafka setup
        binder.bind(KafkaOptions, get_kafka_options(), scope=singleton)
        binder.bind(IKafkaService, KafkaService, scope=singleton)
        binder.bind(CreateKafkaCommandHandler, CreateKafkaCommandHandler, scope=noscope)
        # For CosmosDb Setup
        binder.bind(CosmosDbOptions, get_cosmosdb_options(), scope=singleton)
        binder.bind(ICosmosDbService, CosmosDbService, scope=singleton)
        binder.bind(CreateCosmosDbCommandHandler, CreateCosmosDbCommandHandler, scope=noscope)
        # For RabbitMQ Setup
        binder.bind(RabbitMqOptions, get_rabbitmq_options(), scope=singleton)
        binder.bind(IRabbitMqAdminService, RabbitMqAdminService, scope=singleton)
        binder.bind(CreateRabbitMqCommandHandler, CreateRabbitMqCommandHandler, scope=noscope)
        # For Qdrant Setup
        binder.bind(QdrantOptions, get_qdrant_options(), scope=singleton)
        binder.bind(IQdrantService, QdrantService, scope=singleton)
        binder.bind(CreateQdrantCommandHandler, CreateQdrantCommandHandler, scope=noscope)


injector = create_injector()
