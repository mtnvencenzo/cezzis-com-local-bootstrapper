from abc import ABC, abstractmethod


class IKafkaService(ABC):
    @abstractmethod
    async def create_topic(self, topic_name: str, num_partitions: int | None = None) -> None:
        pass
