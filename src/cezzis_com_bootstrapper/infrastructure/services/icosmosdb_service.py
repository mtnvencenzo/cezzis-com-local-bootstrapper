from abc import ABC, abstractmethod


class ICosmosDbService(ABC):
    @abstractmethod
    async def create_database(self, database_name: str) -> None:
        """Create a Cosmos DB database with the given name

        Args:
            database_name (str): The name of the database to create.
        """
        pass

    @abstractmethod
    async def create_container(self, database_name: str, container_name: str, partitionKeyPath: str) -> None:
        """Create a container in the Cosmos DB database.

        Args:
            container_name (str): The name of the container to create.
            num_partitions (int | None): The number of partitions for the container.
        """
        pass
