import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BootstrapperOptions(BaseSettings):
    """Bootstrapper feature flag options loaded from environment variables and .env files.

    Attributes:
        enable_rabbitmq (bool): Flag to enable RabbitMQ bootstrapping.
        enable_blob_storage (bool): Flag to enable Azure Blob Storage bootstrapping.
        enable_kafka (bool): Flag to enable Kafka bootstrapping.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    enable_rabbitmq: bool = Field(default=True, validation_alias="ENABLE_RABBITMQ")
    enable_blob_storage: bool = Field(default=True, validation_alias="ENABLE_BLOB_STORAGE")
    enable_kafka: bool = Field(default=True, validation_alias="ENABLE_KAFKA")


_logger: logging.Logger = logging.getLogger("bootstrapper_options")

_bootstrapper_options: BootstrapperOptions | None = None


def get_bootstrapper_options() -> BootstrapperOptions:
    """Get the singleton instance of BootstrapperOptions.

    Returns:
        BootstrapperOptions: The bootstrapper options instance.
    """
    global _bootstrapper_options
    if _bootstrapper_options is None:
        _bootstrapper_options = BootstrapperOptions()
        _logger.info(
            "Bootstrapper options loaded: enable_rabbitmq=%s, enable_blob_storage=%s, enable_kafka=%s",
            _bootstrapper_options.enable_rabbitmq,
            _bootstrapper_options.enable_blob_storage,
            _bootstrapper_options.enable_kafka,
        )
    return _bootstrapper_options
