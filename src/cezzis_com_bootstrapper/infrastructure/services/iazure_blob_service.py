from abc import ABC, abstractmethod


class IAzureBlobService(ABC):
    @abstractmethod
    async def create_container(self, container_name: str) -> None:
        pass
