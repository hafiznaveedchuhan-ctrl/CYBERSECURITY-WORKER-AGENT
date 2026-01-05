"""Qdrant client wrapper and collection management."""

from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import structlog

from src.config import settings

logger = structlog.get_logger()


class QdrantService:
    """Qdrant service for managing vector collections."""

    # Collection configurations
    COLLECTIONS = {
        "textbook_chunks": {
            "size": 1536,  # OpenAI text-embedding-3-small
            "distance": Distance.COSINE,
            "description": "SOC textbook content chunks for RAG",
        },
        "chat_history": {
            "size": 1536,
            "distance": Distance.COSINE,
            "description": "Chat history embeddings for context",
        },
    }

    def __init__(self, url: Optional[str] = None):
        self.url = url or settings.qdrant_url
        self.client = QdrantClient(url=self.url)

    async def initialize_collections(self) -> None:
        """Initialize all required collections."""
        existing = {c.name for c in self.client.get_collections().collections}

        for name, config in self.COLLECTIONS.items():
            if name not in existing:
                logger.info("Creating Qdrant collection", collection=name)
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(
                        size=config["size"],
                        distance=config["distance"],
                    ),
                )

                # Add payload indexes for common queries
                self.client.create_payload_index(
                    collection_name=name,
                    field_name="document_id",
                    field_schema=models.PayloadSchemaType.INTEGER,
                )
                self.client.create_payload_index(
                    collection_name=name,
                    field_name="category",
                    field_schema=models.PayloadSchemaType.KEYWORD,
                )
            else:
                logger.debug("Collection already exists", collection=name)

    def get_collection_info(self, collection_name: str) -> dict:
        """Get collection statistics."""
        info = self.client.get_collection(collection_name)
        return {
            "name": collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status.value,
            "config": {
                "size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance.value,
            },
        }

    async def upsert_chunks(
        self,
        collection_name: str,
        ids: list[str],
        vectors: list[list[float]],
        payloads: list[dict],
    ) -> None:
        """Upsert vectors with payloads."""
        points = [
            models.PointStruct(id=id_, vector=vector, payload=payload)
            for id_, vector, payload in zip(ids, vectors, payloads)
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points,
        )
        logger.info("Upserted vectors", collection=collection_name, count=len(points))

    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float = 0.7,
        filter_conditions: Optional[dict] = None,
    ) -> list[dict]:
        """Search for similar vectors."""
        query_filter = None
        if filter_conditions:
            must_conditions = []
            for key, value in filter_conditions.items():
                if isinstance(value, list):
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchAny(any=value),
                        )
                    )
                else:
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value),
                        )
                    )
            query_filter = models.Filter(must=must_conditions)

        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
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
            for result in results
        ]

    async def delete_by_document(
        self,
        collection_name: str,
        document_id: int,
    ) -> None:
        """Delete all vectors for a document."""
        self.client.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id),
                        )
                    ]
                )
            ),
        )
        logger.info("Deleted vectors for document", document_id=document_id)


# Singleton instance
_qdrant_service: Optional[QdrantService] = None


def get_qdrant_service() -> QdrantService:
    """Get the Qdrant service singleton."""
    global _qdrant_service
    if _qdrant_service is None:
        _qdrant_service = QdrantService()
    return _qdrant_service
