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
        self.client = CosmosClient.from_connection_string(self.cosmosdb_options.connection_string)

    async def create_database(self, database_name: str) -> None:
        self.logger.info(f"Creating Cosmos DB database: {database_name}")

        try:
            async for db in self.client.list_databases():
                if db["id"] == database_name:
                    self.logger.info(f"Database {database_name} already exists. Skipping creation.")
                    return
        except Exception as e:
            self.logger.exception(f"Failed to list databases: {e}")
            raise

        try:
            await self.client.create_database(database_name)
            self.logger.info(f"Database {database_name} created successfully.")
        except Exception as e:
            self.logger.exception(f"Failed to create database {database_name}: {e}")
            raise

    async def create_container(self, database_name: str, container_name: str, partitionKeyPath: str) -> None:
        self.logger.info(
            f"Creating Cosmos DB container: {container_name} with partition key: {partitionKeyPath} in database: {database_name}"
        )

        db_client = self.client.get_database_client(database_name)

        try:
            async for container in db_client.list_containers():
                if container["id"] == container_name:
                    self.logger.info(
                        f"Container {container_name} already exists in database {database_name}. Skipping creation."
                    )
                    return
        except Exception as e:
            self.logger.exception(f"Failed to list containers in database {database_name}: {e}")
            raise

        try:
            await db_client.create_container(
                id=container_name, partition_key=PartitionKey(path=partitionKeyPath, kind="Hash", version=2)
            )
            self.logger.info(f"Container {container_name} created successfully in database {database_name}.")
        except Exception as e:
            self.logger.exception(f"Failed to create container {container_name} in database {database_name}: {e}")
            raise
