import asyncio
import logging

from mediatr import Mediator

from cezzis_com_bootstrapper.app_module import injector
from cezzis_com_bootstrapper.application import initialize_opentelemetry
from cezzis_com_bootstrapper.application.concerns.messaging.commands.create_kafka_command import CreateKafkaCommand
from cezzis_com_bootstrapper.application.concerns.storage import (
    CreateBlobStorageCommand,
)

logger = logging.getLogger("main")


async def main():
    """Main entry point for bootstrapping."""
    global logger

    initialize_opentelemetry()
    logger = logging.getLogger("main")
    logger.info("Starting Bootstrapper...")

    mediator = injector.get(Mediator)
    await mediator.send_async(CreateBlobStorageCommand())
    await mediator.send_async(CreateKafkaCommand())

    logger.info("Bootstrapping completed successfully")


def main_entry():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
    finally:
        logger.info("Application shutdown complete.")


if __name__ == "__main__":
    main_entry()
