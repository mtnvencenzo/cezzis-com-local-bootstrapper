import asyncio
import logging

from injector import Injector
from mediatr import Mediator

from cezzis_com_bootstrapper.app_module import AppModule
from cezzis_com_bootstrapper.application import initialize_opentelemetry
from cezzis_com_bootstrapper.application.concerns.storage.commands.create_container_command import (
    CreateContainerCommand,
)

logger = logging.getLogger(__name__)


def create_injector() -> Injector:
    return Injector([AppModule()])


injector = create_injector()


def my_class_handler_manager(handler_class, is_behavior=False):
    if is_behavior:
        # custom logic
        pass

    return injector.get(handler_class)


async def main():
    """Main entry point for bootstrapping."""
    global logger

    initialize_opentelemetry()

    logger = logging.getLogger(__name__)
    logger.info("OpenTelemetry initialized successfully")
    logger.info("Starting Bootstrapper...")

    mediator = Mediator(handler_class_manager=my_class_handler_manager)

    create_container_command = CreateContainerCommand(container_name="my-container")
    result = await mediator.send_async(create_container_command)

    if result:
        logger.info("Container created successfully")
    else:
        logger.error("Failed to create container")

    # TODO: Add your bootstrapping tasks here:
    # - Initialize queues
    # - Setup blob storage
    # - Initialize database
    # - Seed data

    logger.info("Bootstrapping completed successfully")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
    finally:
        logger.info("Application shutdown complete.")
        # shutdown_consumers()


# app = FastAPI()

# app.include_router(injector.get(SemanticSearchRouter))
# app.include_router(injector.get(ConverstionalSearchRouter))
