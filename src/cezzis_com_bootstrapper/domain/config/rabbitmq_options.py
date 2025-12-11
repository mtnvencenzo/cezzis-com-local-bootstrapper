import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMqOptions(BaseSettings):
    """RabbitMQ configuration options loaded from environment variables and .env files.

    Attributes:
        bootstrap_servers (str): RabbitMQ bootstrap servers.
        consumer_group (str): RabbitMQ consumer group ID.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    bootstrap_servers: str = Field(default="", validation_alias="RABBITMQ_BOOTSTRAP_SERVERS")
    consumer_group: str = Field(default="", validation_alias="RABBITMQ_CONSUMER_GROUP")


_logger: logging.Logger = logging.getLogger("rabbitmq_options")

_rabbitmq_options: RabbitMqOptions | None = None


def get_rabbitmq_options() -> RabbitMqOptions:
    """Get the singleton instance of RabbitMqOptions.

    Returns:
        RabbitMqOptions: The RabbitMQ options instance.
    """
    global _rabbitmq_options
    if _rabbitmq_options is None:
        _rabbitmq_options = RabbitMqOptions()

        # Validate required configuration
        if not _rabbitmq_options.bootstrap_servers:
            raise ValueError("RABBITMQ_BOOTSTRAP_SERVERS environment variable is required")
        if not _rabbitmq_options.consumer_group:
            raise ValueError("RABBITMQ_CONSUMER_GROUP environment variable is required")

        _logger.info("RabbitMQ options loaded successfully.")

    return _rabbitmq_options


def clear_rabbitmq_options_cache() -> None:
    """Clear the cached RabbitMqOptions instance."""
    global _rabbitmq_options
    _rabbitmq_options = None
