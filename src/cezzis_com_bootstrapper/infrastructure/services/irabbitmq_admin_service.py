from abc import ABC, abstractmethod
from typing import Any

from cezzis_com_bootstrapper.domain.messaging.rabbitmq_configuration import RabbitMqConfiguration
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_queue import RabbitMqQueue

class IRabbitMqAdminService(ABC):
    @abstractmethod
    async def create_vhost_if_not_exists(self, vhost: str) -> None:
        """Creates a RabbitMQ virtual host if it does not already exist."""
        pass

    @abstractmethod
    async def create_user_if_not_exists(self, username: str, password: str, tags: str = "") -> None:
        """Creates a RabbitMQ user if it does not already exist."""
        pass

    @abstractmethod
    async def assign_vhost_permissions(self, vhost: str, username: str, configure: str = ".*", write: str = ".*", read: str = ".*") -> None:
        """Assigns permissions to a user for a specific virtual host."""
        pass

    @abstractmethod
    async def list_vhost_users(self, vhost: str) -> list[str]:
        """Lists all RabbitMQ users for a specific virtual host."""
        pass

    @abstractmethod
    async def delete_user_from_vhost(self, vhost: str, username: str) -> None:
        """Deletes a RabbitMQ user from a specific virtual host."""
        pass

    @abstractmethod
    async def list_exchanges_in_vhost(self, vhost: str) -> list[str]:
        """Lists all exchanges in a specific virtual host."""
        pass

    @abstractmethod
    async def create_exchange_if_not_exists(self, vhost: str, exchange_def) -> None:
        """Creates an exchange in a specific virtual host."""
        pass

    @abstractmethod
    async def delete_exchange_from_vhost(self, vhost: str, exchange_name: str) -> None:
        """Deletes an exchange from a specific virtual host."""
        pass

    @abstractmethod
    async def list_queues_in_vhost(self, vhost: str) -> list[str]:
        """Lists all exchanges in a specific virtual host."""
        pass

    @abstractmethod
    async def create_queue_for_vhost(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host."""
        pass

    @abstractmethod
    async def create_queue_if_not_exists(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host if it does not already exist."""
        pass

    @abstractmethod
    async def delete_queue_for_vhost(self, vhost: str, queue_name: str) -> None:
        """Deletes a queue from a specific virtual host."""
        pass

    @abstractmethod
    async def LoadFromFileAsync(self, file_path: str) -> RabbitMqConfiguration:
        """Loads RabbitMQ configuration from a JSON file."""
        pass