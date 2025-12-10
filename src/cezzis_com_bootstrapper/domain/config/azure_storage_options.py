import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureStorageOptions(BaseSettings):
    """Azure storage configuration options loaded from environment variables and .env files.

    Attributes:
        connection_string (str): Azure storage connection string.
        account_avatars_container_name (str): Azure storage container name for account avatars.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    connection_string: str = Field(default="", validation_alias="AZURE_STORAGE_CONNECTION_STRING")
    account_avatars_container_name: str = Field(default="", validation_alias="ACCOUNT_AVATARS_CONTAINER_NAME")


_logger: logging.Logger = logging.getLogger("azure_storage_options")

_azure_storage_options: AzureStorageOptions | None = None


def get_azure_storage_options() -> AzureStorageOptions:
    """Get the singleton instance of AzureStorageOptions.

    Returns:
        AzureStorageOptions: The Azure storage options instance.
    """
    global _azure_storage_options
    if _azure_storage_options is None:
        _azure_storage_options = AzureStorageOptions()

        # Validate required configuration
        if not _azure_storage_options.connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")
        if not _azure_storage_options.account_avatars_container_name:
            raise ValueError("ACCOUNT_AVATARS_CONTAINER_NAME environment variable is required")

        _logger.info("Azure storage options loaded successfully.")

    return _azure_storage_options


def clear_azure_storage_options_cache() -> None:
    """Clear the cached AzureStorageOptions instance."""
    global _azure_storage_options
    _azure_storage_options = None
