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
