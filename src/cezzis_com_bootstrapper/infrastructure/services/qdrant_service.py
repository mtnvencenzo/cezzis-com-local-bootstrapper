import asyncio
import logging

from injector import inject
from qdrant_client import QdrantClient, models

from cezzis_com_bootstrapper.domain.config.qdrant_options import QdrantOptions
from cezzis_com_bootstrapper.infrastructure.services.iqdrant_service import IQdrantService


class QdrantService(IQdrantService):
    @inject
    def __init__(self, qdrant_options: QdrantOptions):
        self.logger = logging.getLogger("qdrant_service")
        self.qdrant_client = QdrantClient(
            host=qdrant_options.host,
            port=qdrant_options.port,
            https=qdrant_options.use_https,
            api_key=qdrant_options.api_key if qdrant_options.api_key else None,
            timeout=90,
        )

    async def create_collection_if_not_exists(self, collection_name: str, vector_size: int):
        existing_collections = await asyncio.to_thread(self.qdrant_client.get_collections)
        collection_names = [col.name for col in existing_collections.collections]

        if collection_name not in collection_names:
            self.logger.info(
                f"Creating QDrant collection '{collection_name}' with vector size {vector_size}",
                extra={
                    "collection_name": collection_name,
                    "vector_size": vector_size,
                },
            )
            await asyncio.to_thread(
                self.qdrant_client.create_collection,
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )
            self.logger.info(
                f"Collection '{collection_name}' created.",
                extra={
                    "collection_name": collection_name,
                    "vector_size": vector_size,
                },
            )
