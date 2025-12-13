import logging

from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.domain.config import CosmosDbOptions
from cezzis_com_bootstrapper.infrastructure.services import ICosmosDbService


class CreateCosmosDbCommand(GenericQuery[bool]):
    """Command to initialize CosmosDb and all infrastructure dependencies."""

    pass


@Mediator.handler
class CreateCosmosDbCommandHandler:
    """Command handler for the CreateCosmosDbCommand.

    Args:
        cosmos_db_service (ICosmosDbService): The Cosmos DB service.
        cosmos_db_options (CosmosDbOptions): The Cosmos DB configuration options.
    """

    @inject
    def __init__(self, cosmos_db_service: ICosmosDbService, cosmos_db_options: CosmosDbOptions):
        self.cosmos_db_service = cosmos_db_service
        self.cosmos_db_options = cosmos_db_options
        self.logger = logging.getLogger("create_cosmosdb_command_handler")

    async def handle(self, request: CreateCosmosDbCommand) -> bool:
        await self.cosmos_db_service.create_database(self.cosmos_db_options.cocktails_database_name)

        container_defs = str.split(self.cosmos_db_options.cocktails_container_defs, ",")

        for container_def in container_defs:
            container_info = str.split(container_def, ":")
            container_name = container_info[0]
            partition_key = container_info[1]

            self.logger.info(f"Creating container {container_name} with partition key {partition_key}")
            await self.cosmos_db_service.create_container(
                self.cosmos_db_options.cocktails_database_name, container_name, partition_key
            )

        return True
