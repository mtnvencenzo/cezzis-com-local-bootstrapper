import logging

from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient
from injector import inject

from cezzis_com_bootstrapper.domain.config import CosmosDbOptions
from cezzis_com_bootstrapper.infrastructure.services.icosmosdb_service import ICosmosDbService


class CosmosDbService(ICosmosDbService):
    @inject
    def __init__(self, cosmosdb_options: CosmosDbOptions) -> None:
        self.cosmosdb_options = cosmosdb_options
        self.logger = logging.getLogger("cosmosdb_service")
        self.client = CosmosClient(
            url=self.cosmosdb_options.account_endpoint,
            credential=self.cosmosdb_options.account_key,
            connection_verify=False,
        )

    async def create_database(self, database_name: str) -> None:
        """Create a Cosmos DB database if it does not already exist.

        Args:
            database_name (str): The name of the database to create.
        """
        self.logger.info(f"Creating Cosmos DB database: {database_name}", extra={"database_name": database_name})

        try:
            async for db in self.client.list_databases():
                if db["id"] == database_name:
                    self.logger.info(
                        f"Database {database_name} already exists. Skipping creation.",
                        extra={"database_name": database_name},
                    )
                    return
        except Exception as e:
            self.logger.exception("Failed to list databases", extra={"error": str(e), "database_name": database_name})
            raise

        try:
            await self.client.create_database(database_name)
            self.logger.info(f"Database {database_name} created successfully.", extra={"database_name": database_name})
        except Exception as e:
            self.logger.exception(
                f"Failed to create database {database_name}", extra={"error": str(e), "database_name": database_name}
            )
            raise

    async def create_container(self, database_name: str, container_name: str, partitionKeyPath: str) -> None:
        """Create a Cosmos DB container if it does not already exist.

        Args:
            database_name (str): The name of the database.
            container_name (str): The name of the container to create.
            partitionKeyPath (str): The partition key path for the container.
        """

        self.logger.info(
            f"Creating Cosmos DB container: {container_name} with partition key: {partitionKeyPath} in database: {database_name}",
            extra={"database_name": database_name, "container_name": container_name, "partition_key": partitionKeyPath},
        )

        db_client = self.client.get_database_client(database_name)

        try:
            async for container in db_client.list_containers():
                if container["id"] == container_name:
                    self.logger.info(
                        f"Container {container_name} already exists in database {database_name}. Skipping creation.",
                        extra={
                            "database_name": database_name,
                            "container_name": container_name,
                            "partition_key": partitionKeyPath,
                        },
                    )
                    return
        except Exception as e:
            self.logger.exception(
                f"Failed to list containers in database {database_name}",
                extra={
                    "error": str(e),
                    "database_name": database_name,
                    "container_name": container_name,
                    "partition_key": partitionKeyPath,
                },
            )
            raise

        try:
            await db_client.create_container(
                id=container_name, partition_key=PartitionKey(path=partitionKeyPath, kind="Hash", version=2)
            )
            self.logger.info(
                f"Container {container_name} created successfully in database {database_name}.",
                extra={
                    "database_name": database_name,
                    "container_name": container_name,
                    "partition_key": partitionKeyPath,
                },
            )
        except Exception as e:
            self.logger.exception(
                f"Failed to create container {container_name} in database {database_name}",
                extra={
                    "error": str(e),
                    "database_name": database_name,
                    "container_name": container_name,
                    "partition_key": partitionKeyPath,
                },
            )
            raise
