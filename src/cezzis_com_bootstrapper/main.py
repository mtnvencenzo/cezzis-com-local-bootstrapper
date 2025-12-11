import asyncio
import logging

from mediatr import Mediator

from cezzis_com_bootstrapper.app_module import injector
from cezzis_com_bootstrapper.application import initialize_opentelemetry
from cezzis_com_bootstrapper.application.concerns.storage.commands.create_containers_command import (
    CreateContainersCommand,
)

logger = logging.getLogger("main")


async def main():
    """Main entry point for bootstrapping."""
    global logger

    initialize_opentelemetry()
    logger = logging.getLogger("main")
    logger.info("Starting Bootstrapper...")

    mediator = injector.get(Mediator)
    await mediator.send_async(CreateContainersCommand())

    logger.info("Bootstrapping completed successfully")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
    finally:
        logger.info("Application shutdown complete.")
