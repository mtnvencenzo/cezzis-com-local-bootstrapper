import logging

from confluent_kafka.admin import AdminClient, NewTopic
from injector import inject

from cezzis_com_bootstrapper.domain.config import KafkaOptions
from cezzis_com_bootstrapper.infrastructure.services.ikafka_service import IKafkaService


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
                "ssl.ca.location": self.kafka_options.ssl_ca_location,
            },
            logger=self.logger,
        )

        if num_partitions is None:
            num_partitions = self.kafka_options.default_topic_partitions

        existing_topics = admin_client.list_topics().topics

        if topic_name in existing_topics:
            self.logger.info(f"Topic {topic_name} already exists. Skipping creation.")
            return

        topics = [NewTopic(topic=topic_name, num_partitions=num_partitions)]

        futures = admin_client.create_topics(topics)

        for topic, future in futures.items():
            try:
                future.result()
            except Exception:
                self.logger.exception(f"Failed to create topic {topic}")
                raise
