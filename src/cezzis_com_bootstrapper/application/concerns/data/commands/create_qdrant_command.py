import logging

from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.domain.config.qdrant_options import QdrantOptions
from cezzis_com_bootstrapper.infrastructure.services.iqdrant_service import IQdrantService


class CreateQdrantCommand(GenericQuery[bool]):
    """Command to initialize Qdrant and all infrastructure dependencies."""

    pass


@Mediator.handler
class CreateQdrantCommandHandler:
    """Command handler for the CreateQdrantCommand.

    Args:
        qdrant_service (IQdrantService): The Qdrant service.
        qdrant_options (QdrantOptions): The Qdrant configuration options.
    """

    @inject
    def __init__(self, qdrant_service: IQdrantService, qdrant_options: QdrantOptions):
        self.qdrant_service = qdrant_service
        self.qdrant_options = qdrant_options
        self.logger = logging.getLogger("create_qdrant_command_handler")

    async def handle(self, request: CreateQdrantCommand) -> bool:
        await self.qdrant_service.create_collection_if_not_exists(
            collection_name=self.qdrant_options.collection_name,
            vector_size=self.qdrant_options.vector_size,
        )
        return True
