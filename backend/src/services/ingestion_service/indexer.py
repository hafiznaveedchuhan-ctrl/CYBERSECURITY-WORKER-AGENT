"""Qdrant indexer for vector storage."""

from typing import Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
import structlog

from src.config import settings
from src.services.rag_service.embeddings import EmbeddingsService
from src.services.ingestion_service.chunker import Chunk

logger = structlog.get_logger()


class QdrantIndexer:
    """Indexes document chunks in Qdrant."""

    def __init__(self, collection_name: str = "textbook_chunks"):
        """
        Initialize indexer.

        Args:
            collection_name: Qdrant collection name
        """
        self.collection_name = collection_name
        self.client: Optional[AsyncQdrantClient] = None
        self.embeddings = EmbeddingsService()
        self.vector_size = 1536  # text-embedding-3-small

    async def initialize(self):
        """Initialize Qdrant client and ensure collection exists."""
        self.client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
        )

        # Create collection if it doesn't exist
        collections = await self.client.get_collections()
        collection_names = [c.name for c in collections.collections]

        if self.collection_name not in collection_names:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(
                "Collection created",
                collection=self.collection_name,
                vector_size=self.vector_size,
            )
        else:
            logger.info(
                "Collection exists",
                collection=self.collection_name,
            )

    async def index_chunk(self, chunk: Chunk) -> str:
        """
        Index a single chunk.

        Args:
            chunk: Chunk to index

        Returns:
            Point ID
        """
        if not self.client:
            raise RuntimeError("Indexer not initialized")

        # Generate embedding
        embedding = await self.embeddings.embed_text(chunk.content)

        # Create point
        point = PointStruct(
            id=chunk.id,
            vector=embedding,
            payload=chunk.to_dict(),
        )

        # Upsert to Qdrant
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

        logger.debug(
            "Chunk indexed",
            chunk_id=chunk.id,
            module=chunk.module,
            content_length=len(chunk.content),
        )

        return chunk.id

    async def index_chunks(self, chunks: list[Chunk], batch_size: int = 100) -> int:
        """
        Index multiple chunks in batches.

        Args:
            chunks: List of chunks to index
            batch_size: Number of chunks per batch

        Returns:
            Number of chunks indexed
        """
        if not self.client:
            raise RuntimeError("Indexer not initialized")

        total_indexed = 0

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            # Generate embeddings for batch
            texts = [c.content for c in batch]
            embeddings = await self.embeddings.embed_batch(texts)

            # Create points
            points = [
                PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload=chunk.to_dict(),
                )
                for chunk, embedding in zip(batch, embeddings)
            ]

            # Upsert batch
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            total_indexed += len(batch)

            logger.info(
                "Batch indexed",
                batch_num=i // batch_size + 1,
                batch_size=len(batch),
                total_indexed=total_indexed,
            )

        return total_indexed

    async def delete_by_module(self, module: str) -> int:
        """
        Delete all chunks for a module.

        Args:
            module: Module identifier

        Returns:
            Number of points deleted
        """
        if not self.client:
            raise RuntimeError("Indexer not initialized")

        from qdrant_client.models import Filter, FieldCondition, MatchValue

        # Delete by filter
        result = await self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="module",
                        match=MatchValue(value=module),
                    )
                ]
            ),
        )

        logger.info(
            "Module chunks deleted",
            module=module,
        )

        return 0  # Qdrant doesn't return count directly

    async def get_collection_stats(self) -> dict:
        """Get collection statistics."""
        if not self.client:
            raise RuntimeError("Indexer not initialized")

        info = await self.client.get_collection(self.collection_name)

        return {
            "collection": self.collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status.value,
        }

    async def close(self):
        """Close Qdrant client."""
        if self.client:
            await self.client.close()
            logger.info("Qdrant client closed")
