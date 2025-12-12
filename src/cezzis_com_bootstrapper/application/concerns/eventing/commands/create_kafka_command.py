from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.domain.config import KafkaOptions
from cezzis_com_bootstrapper.infrastructure.services import IKafkaService


class CreateKafkaCommand(GenericQuery[bool]):
    """Command to initialize Kafka and all infrastructure dependencies."""

    pass


@Mediator.handler
class CreateKafkaCommandHandler:
    """Command handler for the CreateKafkaCommand."""

    @inject
    def __init__(self, kafka_service: IKafkaService, kafka_options: KafkaOptions):
        self.kafka_service = kafka_service
        self.kafka_options = kafka_options

    async def handle(self, request: CreateKafkaCommand) -> bool:
        await self.kafka_service.create_topic(self.kafka_options.cocktails_update_topic_name)
        return True
