import logging

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
        self.logger = logging.getLogger("create_kafka_command_handler")

    async def handle(self, request: CreateKafkaCommand) -> bool:
        topic_defs = str.split(self.kafka_options.cocktails_topic_defs, ",")

        for topic_def in topic_defs:
            topic_info = str.split(topic_def, ":")
            topic_name = topic_info[0]
            partitions = len(topic_info) > 1 and int(topic_info[1]) or 0

            self.logger.info(f"Creating topic {topic_name} with {partitions} partitions")
            await self.kafka_service.create_topic(
                topic_name=topic_name,
                num_partitions=partitions <= 0 and self.kafka_options.default_topic_partitions or partitions,
            )

        return True
