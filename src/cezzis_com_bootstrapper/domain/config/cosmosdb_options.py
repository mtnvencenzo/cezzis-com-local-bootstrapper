import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CosmosDbOptions(BaseSettings):
    """Cosmos DB configuration options loaded from environment variables and .env files.

    Attributes:
        account_key (str): The account key for the Cosmos DB account.
        account_endpoint (str): The account endpoint for the Cosmos DB account.
        cocktails_database_name (str): The name of the cocktails database.
        cocktails_container_defs (str): The comma separated list of the cocktails container definitions (container1>:/partitionKey,container2>:/partitionKey).
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    account_key: str = Field(default="", validation_alias="COSMOSDB_ACCOUNT_KEY")
    account_endpoint: str = Field(default="", validation_alias="COSMOSDB_ACCOUNT_ENDPOINT")
    cocktails_database_name: str = Field(default="", validation_alias="COSMOSDB_COCKTAILS_DATABASE_NAME")
    cocktails_container_defs: str = Field(default="", validation_alias="COSMOSDB_COCKTAILS_CONTAINER_DEFS")


_logger: logging.Logger = logging.getLogger("cosmosdb_options")

_cosmosdb_options: CosmosDbOptions | None = None


def get_cosmosdb_options() -> CosmosDbOptions:
    """Get the singleton instance of CosmosDbOptions.

    Returns:
        CosmosDbOptions: The Cosmos DB options instance.
    """
    global _cosmosdb_options
    if _cosmosdb_options is None:
        _cosmosdb_options = CosmosDbOptions()

        # Validate required configuration
        if not _cosmosdb_options.account_key:
            raise ValueError("COSMOSDB_ACCOUNT_KEY environment variable is required")
        if not _cosmosdb_options.account_endpoint:
            raise ValueError("COSMOSDB_ACCOUNT_ENDPOINT environment variable is required")
        if not _cosmosdb_options.cocktails_database_name:
            raise ValueError("COSMOSDB_COCKTAILS_DATABASE_NAME environment variable is required")
        if not _cosmosdb_options.cocktails_container_defs:
            raise ValueError("COSMOSDB_COCKTAILS_CONTAINER_DEFS environment variable is required")

        _logger.info("Cosmos DB options loaded successfully.")

    return _cosmosdb_options


def clear_cosmosdb_options_cache() -> None:
    """Clear the cached CosmosDbOptions instance."""
    global _cosmosdb_options
    _cosmosdb_options = None
