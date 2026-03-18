from abc import ABC, abstractmethod


class IQdrantService(ABC):
    @abstractmethod
    async def create_collection_if_not_exists(self, collection_name: str, vector_size: int):
        """Creates a QDrant collection if it does not already exist.

        Args:
            collection_name (str): The name of the collection to create.
            vector_size (int): The size of the vectors to be stored in the collection.
        """
        pass

    @abstractmethod
    async def create_index_if_not_exists(self, collection_name: str, field_name: str, field_schema: str):
        """Creates an index on a QDrant collection if it does not already exist.

        Args:
            collection_name (str): The name of the collection to create the index on.
            field_name (str): The name of the field to create the index for.
            field_schema: The schema type of the field to be indexed.
        """
        pass
