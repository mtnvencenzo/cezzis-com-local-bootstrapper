import logging
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CosmosDbOptions(BaseSettings):
    """Cosmos DB configuration options loaded from environment variables and .env files.

    Attributes:
        database_name (str): The name of the cosmos database.
        connection_string (str): The connection string for the Cosmos DB account.
        cocktails_container_name (str): The name of the cocktails container.
        ingredients_container_name (str): The name of the ingredients container.
        accounts_container_name (str): The name of the accounts container.
        account_key (str): The account key for the Cosmos DB account.
        account_endpoint (str): The account endpoint for the Cosmos DB account.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{os.environ.get('ENV')}"), env_file_encoding="utf-8", extra="allow"
    )

    database_name: str = Field(default="", validation_alias="COSMOSDB_DATABASE_NAME")
    connection_string: str = Field(default="", validation_alias="COSMOSDB_CONNECTION_STRING")
    cocktails_container_name: str = Field(default="", validation_alias="COSMOSDB_COCKTAILS_CONTAINER_NAME")
    ingredients_container_name: str = Field(default="", validation_alias="COSMOSDB_INGREDIENTS_CONTAINER_NAME")
    accounts_container_name: str = Field(default="", validation_alias="COSMOSDB_ACCOUNTS_CONTAINER_NAME")
    account_key: str = Field(default="", validation_alias="COSMOSDB_ACCOUNT_KEY")
    account_endpoint: str = Field(default="", validation_alias="COSMOSDB_ACCOUNT_ENDPOINT")


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
        if not _cosmosdb_options.database_name:
            raise ValueError("COSMOSDB_DATABASE_NAME environment variable is required")
        if not _cosmosdb_options.connection_string:
            raise ValueError("COSMOSDB_CONNECTION_STRING environment variable is required")
        if not _cosmosdb_options.cocktails_container_name:
            raise ValueError("COSMOSDB_COCKTAILS_CONTAINER_NAME environment variable is required")
        if not _cosmosdb_options.ingredients_container_name:
            raise ValueError("COSMOSDB_INGREDIENTS_CONTAINER_NAME environment variable is required")
        if not _cosmosdb_options.accounts_container_name:
            raise ValueError("COSMOSDB_ACCOUNTS_CONTAINER_NAME environment variable is required")
        if not _cosmosdb_options.account_key:
            raise ValueError("COSMOSDB_ACCOUNT_KEY environment variable is required")
        if not _cosmosdb_options.account_endpoint:
            raise ValueError("COSMOSDB_ACCOUNT_ENDPOINT environment variable is required")

        _logger.info("Cosmos DB options loaded successfully.")

    return _cosmosdb_options


def clear_cosmosdb_options_cache() -> None:
    """Clear the cached CosmosDbOptions instance."""
    global _cosmosdb_options
    _cosmosdb_options = None
