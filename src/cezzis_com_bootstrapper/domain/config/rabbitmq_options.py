import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMqOptions(BaseSettings):
    """RabbitMQ configuration options loaded from environment variables and .env files.

    Attributes:
        vhost (str): The virtual host name for RabbitMQ.
        host (str): RabbitMQ server host.
        port (int): RabbitMQ server port.
        admin_port (int): RabbitMQ management plugin port.
        admin_username (str): RabbitMQ administrator username.
        admin_password (str): RabbitMQ administrator password.
        app_username (str): RabbitMQ application username.
        app_password (str): RabbitMQ application password.
        app_config_file_path (str): Path to the custom rabbit mq configuration file.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    vhost: str = Field(default="", validation_alias="RABBITMQ_VHOST")
    host: str = Field(default="", validation_alias="RABBITMQ_HOST")
    port: int = Field(default=0, validation_alias="RABBITMQ_PORT")
    admin_port: int = Field(default=0, validation_alias="RABBITMQ_ADMIN_PORT")
    admin_username: str = Field(default="", validation_alias="RABBITMQ_ADMIN_USERNAME")
    admin_password: str = Field(default="", validation_alias="RABBITMQ_ADMIN_PASSWORD")
    app_username: str = Field(default="", validation_alias="RABBITMQ_APP_USERNAME")
    app_password: str = Field(default="", validation_alias="RABBITMQ_APP_PASSWORD")
    app_config_file_path: str = Field(default="", validation_alias="RABBITMQ_APP_CONFIG_FILE_PATH")


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
        if not _rabbitmq_options.vhost:
            raise ValueError("RABBITMQ_VHOST is required but not set.")
        if not _rabbitmq_options.host:
            raise ValueError("RABBITMQ_HOST is required but not set.")
        if not _rabbitmq_options.port:
            raise ValueError("RABBITMQ_PORT is required but not set.")
        if not _rabbitmq_options.admin_port:
            raise ValueError("RABBITMQ_ADMIN_PORT is required but not set.")
        if not _rabbitmq_options.admin_username:
            raise ValueError("RABBITMQ_ADMIN_USERNAME is required but not set.")
        if not _rabbitmq_options.admin_password:
            raise ValueError("RABBITMQ_ADMIN_PASSWORD is required but not set.")
        if not _rabbitmq_options.app_username:
            raise ValueError("RABBITMQ_APP_USERNAME is required but not set.")
        if not _rabbitmq_options.app_password:
            raise ValueError("RABBITMQ_APP_PASSWORD is required but not set.")

        _logger.info("RabbitMQ options loaded successfully.")

    return _rabbitmq_options


def clear_rabbitmq_options_cache() -> None:
    """Clear the cached RabbitMqOptions instance."""
    global _rabbitmq_options
    _rabbitmq_options = None
