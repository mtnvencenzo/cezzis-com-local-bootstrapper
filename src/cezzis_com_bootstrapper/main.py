import asyncio
import logging
import sys

from mediatr import Mediator

from cezzis_com_bootstrapper.app_module import injector
from cezzis_com_bootstrapper.application import initialize_opentelemetry
from cezzis_com_bootstrapper.application.behaviors.exception_handling.global_exception_handler import (
    global_exception_handler,
)
from cezzis_com_bootstrapper.application.concerns import (
    CreateBlobStorageCommand,
    CreateKafkaCommand,
    CreateRabbitMqCommand,
)
from cezzis_com_bootstrapper.domain.config import BootstrapperOptions

sys.excepthook = global_exception_handler

logger = logging.getLogger("main")


async def main():
    """Main entry point for bootstrapping."""
    global logger

    initialize_opentelemetry()
    logger = logging.getLogger("main")
    logger.info("Starting Bootstrapper...")

    mediator = injector.get(Mediator)
    options = injector.get(BootstrapperOptions)

    if options.enable_rabbitmq:
        await mediator.send_async(CreateRabbitMqCommand())
    else:
        logger.info("RabbitMQ bootstrapping is disabled, skipping...")

    if options.enable_blob_storage:
        await mediator.send_async(CreateBlobStorageCommand())
    else:
        logger.info("Blob Storage bootstrapping is disabled, skipping...")

    if options.enable_kafka:
        await mediator.send_async(CreateKafkaCommand())
    else:
        logger.info("Kafka bootstrapping is disabled, skipping...")

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
