import asyncio
import logging

from confluent_kafka.admin import AdminClient, NewTopic
from injector import inject

from cezzis_com_bootstrapper.domain.config import KafkaOptions
from cezzis_com_bootstrapper.infrastructure.services.ikafka_service import IKafkaService

_KAFKA_TIMEOUT_SECONDS = 30
_KAFKA_SOCKET_TIMEOUT_MS = 120000
_KAFKA_REQUEST_TIMEOUT_MS = 120000
_KAFKA_METADATA_MAX_AGE_MS = 120000


class KafkaService(IKafkaService):
    @inject
    def __init__(self, kafka_options: KafkaOptions) -> None:
        self.kafka_options = kafka_options
        self.logger = logging.getLogger("kafka_service")

    async def create_topic(self, topic_name: str, num_partitions: int | None = None) -> None:
        admin_client = AdminClient(
            conf={
                "bootstrap.servers": self.kafka_options.bootstrap_servers,
                "security.protocol": self.kafka_options.security_protocol,
                "socket.timeout.ms": _KAFKA_SOCKET_TIMEOUT_MS,
                "request.timeout.ms": _KAFKA_REQUEST_TIMEOUT_MS,
                "metadata.max.age.ms": _KAFKA_METADATA_MAX_AGE_MS,
            },
            logger=self.logger,
        )

        if num_partitions is None:
            num_partitions = self.kafka_options.default_topic_partitions

        existing_topics = (await asyncio.to_thread(admin_client.list_topics, timeout=_KAFKA_TIMEOUT_SECONDS)).topics

        if topic_name in existing_topics:
            self.logger.info(f"Topic {topic_name} already exists. Skipping creation.")
            return

        topics = [NewTopic(topic=topic_name, num_partitions=num_partitions)]

        futures = await asyncio.to_thread(admin_client.create_topics, topics, operation_timeout=_KAFKA_TIMEOUT_SECONDS)

        for topic, future in futures.items():
            try:
                future.result()
            except Exception:
                self.logger.exception(f"Failed to create topic {topic}")
                raise
