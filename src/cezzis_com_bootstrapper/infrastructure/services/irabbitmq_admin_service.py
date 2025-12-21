from abc import ABC, abstractmethod

from cezzis_com_bootstrapper.domain.messaging.rabbitmq_binding import RabbitMqBinding
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_configuration import RabbitMqConfiguration
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_queue import RabbitMqQueue


class IRabbitMqAdminService(ABC):
    @abstractmethod
    async def load_from_file(self, file_path: str) -> RabbitMqConfiguration:
        """Loads RabbitMQ configuration from a JSON file.

        Args:
            file_path (str): The path to the JSON configuration file.

        Returns:
            RabbitMqConfiguration: The loaded RabbitMQ configuration.

        """
        pass

    @abstractmethod
    async def create_vhost_if_not_exists(self, vhost: str) -> None:
        """Creates a RabbitMQ virtual host if it does not already exist.

        Args:
            vhost (str): The name of the virtual host to create.

        """
        pass

    @abstractmethod
    async def create_user_if_not_exists(self, username: str, password: str, tags: str = "") -> None:
        """Creates a RabbitMQ user if it does not already exist.

        Args:
            username (str): The username of the RabbitMQ user.
            password (str): The password for the RabbitMQ user.
            tags (str, optional): Comma-separated list of tags for the user. Defaults to "".

        """
        pass

    @abstractmethod
    async def assign_vhost_permissions(
        self, vhost: str, username: str, configure: str = ".*", write: str = ".*", read: str = ".*"
    ) -> None:
        """Assigns permissions to a user for a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.
            username (str): The username of the RabbitMQ user.
            configure (str, optional): The configure permission regex. Defaults to ".*".
            write (str, optional): The write permission regex. Defaults to ".*".
            read (str, optional): The read permission regex. Defaults to ".*".

        """
        pass

    @abstractmethod
    async def list_vhost_users(self, vhost: str) -> list[str]:
        """Lists all RabbitMQ users for a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.

        Returns:
            list[str]: A list of usernames associated with the virtual host.

        """
        pass

    @abstractmethod
    async def delete_user(self, username: str) -> None:
        """Deletes a RabbitMQ user.

        Args:
            username (str): The username of the RabbitMQ user.

        """
        pass

    @abstractmethod
    async def list_exchanges_in_vhost(self, vhost: str) -> list[str]:
        """Lists all exchanges in a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.

        Returns:
            list[str]: A list of exchange names in the virtual host.

        """
        pass

    @abstractmethod
    async def create_exchange_if_not_exists(self, vhost: str, exchange_def) -> None:
        """Creates an exchange in a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.
            exchange_def (RabbitMqExchange): The definition of the exchange to create.

        """
        pass

    @abstractmethod
    async def delete_exchange_from_vhost(self, vhost: str, exchange_name: str) -> None:
        """Deletes an exchange from a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.
            exchange_name (str): The name of the exchange to delete.

        """
        pass

    @abstractmethod
    async def list_queues_in_vhost(self, vhost: str) -> list[str]:
        """Lists all queues in a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.

        Returns:
            list[str]: A list of queue names in the virtual host.

        """
        pass

    @abstractmethod
    async def create_queue_for_vhost(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.
            queue_def (RabbitMqQueue): The definition of the queue to create.

        """
        pass

    @abstractmethod
    async def create_queue_if_not_exists(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host if it does not already exist.

        Args:
            vhost (str): The name of the virtual host.
            queue_def (RabbitMqQueue): The definition of the queue to create.

        """
        pass

    @abstractmethod
    async def delete_queue_for_vhost(self, vhost: str, queue_name: str) -> None:
        """Deletes a queue from a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.
            queue_name (str): The name of the queue to delete.

        """
        pass

    @abstractmethod
    async def list_bindings_in_vhost(self, vhost: str) -> list[RabbitMqBinding]:
        """Lists all bindings in a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.

        Returns:
            list[RabbitMqBinding]: A list of RabbitMqBinding objects representing the bindings.

        """
        pass

    @abstractmethod
    async def create_binding_if_not_exists(self, vhost: str, binding_def: RabbitMqBinding) -> None:
        """Creates a binding in a specific virtual host if it does not already exist.

        Args:
            vhost (str): The name of the virtual host.
            binding_def (RabbitMqBinding): The definition of the binding to create.

        """
        pass

    @abstractmethod
    async def delete_binding_from_vhost(self, vhost: str, binding_def: RabbitMqBinding) -> None:
        """Deletes a binding from a specific virtual host.

        Args:
            vhost (str): The name of the virtual host.
            binding_def (RabbitMqBinding): The definition of the binding to delete.

        """
        pass
