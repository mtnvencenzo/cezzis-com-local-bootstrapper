from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.domain.config import CosmosDbOptions
from cezzis_com_bootstrapper.infrastructure.services import ICosmosDbService


class CreateCosmosDbCommand(GenericQuery[bool]):
    """Command to initialize CosmosDb and all infrastructure dependencies."""

    pass


@Mediator.handler
class CreateCosmosDbCommandHandler:
    """Command handler for the CreateCosmosDbCommand."""

    @inject
    def __init__(self, cosmos_db_service: ICosmosDbService, cosmos_db_options: CosmosDbOptions):
        self.cosmos_db_service = cosmos_db_service
        self.cosmos_db_options = cosmos_db_options

    async def handle(self, request: CreateCosmosDbCommand) -> bool:
        await self.cosmos_db_service.create_database(self.cosmos_db_options.database_name)

        await self.cosmos_db_service.create_container(
            self.cosmos_db_options.database_name, self.cosmos_db_options.cocktails_container_name, "/id"
        )

        await self.cosmos_db_service.create_container(
            self.cosmos_db_options.database_name, self.cosmos_db_options.ingredients_container_name, "/id"
        )

        await self.cosmos_db_service.create_container(
            self.cosmos_db_options.database_name, self.cosmos_db_options.accounts_container_name, "/subjectId"
        )

        return True
