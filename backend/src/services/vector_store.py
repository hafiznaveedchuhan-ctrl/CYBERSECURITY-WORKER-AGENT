"""Vector store service using Qdrant."""

from typing import Optional
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import structlog

from src.config import settings

logger = structlog.get_logger()


class VectorStoreService:
    """Service for managing vector storage in Qdrant."""

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
        self.url = url or settings.qdrant_url
        self.api_key = api_key or getattr(settings, 'qdrant_api_key', '')
        self.collection_name = collection_name or settings.qdrant_collection
        if self.api_key:
            self.client = QdrantClient(url=self.url, api_key=self.api_key)
        else:
            self.client = QdrantClient(url=self.url)
        self.vector_size = 1536  # OpenAI text-embedding-3-small dimension

    async def ensure_collection(self) -> None:
        """Ensure the collection exists, create if not."""
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if not exists:
            logger.info("Creating Qdrant collection", collection=self.collection_name)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    async def upsert_vectors(
        self,
        vectors: list[list[float]],
        payloads: list[dict],
        ids: Optional[list[str]] = None,
    ) -> list[str]:
        """Insert or update vectors in the collection."""
        if ids is None:
            ids = [str(uuid4()) for _ in vectors]

        points = [
            PointStruct(id=id_, vector=vector, payload=payload)
            for id_, vector, payload in zip(ids, vectors, payloads)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

        logger.info("Upserted vectors", count=len(points))
        return ids

    async def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float = 0.7,
        filter_conditions: Optional[dict] = None,
    ) -> list[dict]:
        """Search for similar vectors."""
        try:
            query_filter = None
            if filter_conditions:
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value),
                        )
                        for key, value in filter_conditions.items()
                    ]
                )

            # Use query_points for qdrant-client >= 1.7.0
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter,
            )

            return [
                {
                    "id": str(result.id),
                    "score": result.score,
                    "payload": result.payload,
                }
                for result in results.points
            ]
        except Exception as e:
            logger.warning("Vector search failed, returning empty results", error=str(e))
            return []

    async def delete_by_filter(self, filter_conditions: dict) -> None:
        """Delete vectors matching filter conditions."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value),
                        )
                        for key, value in filter_conditions.items()
                    ]
                )
            ),
        )
        logger.info("Deleted vectors", filter=filter_conditions)

    async def get_collection_info(self) -> dict:
        """Get collection statistics."""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status.value,
        }
