"""RAG (Retrieval Augmented Generation) service."""

from typing import Optional

import structlog

from src.services.vector_store import VectorStoreService
from src.services.embedding import EmbeddingService
from src.config import settings

logger = structlog.get_logger()


class RAGService:
    """Service for RAG-based question answering."""

    def __init__(
        self,
        vector_store: Optional[VectorStoreService] = None,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        self.vector_store = vector_store or VectorStoreService()
        self.embedding_service = embedding_service or EmbeddingService()

    async def retrieve(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
    ) -> list[dict]:
        """Retrieve relevant documents for a query."""
        # Generate query embedding
        query_embedding = await self.embedding_service.embed_text(query)

        # Build filter conditions
        filter_conditions = {}
        if category:
            filter_conditions["category"] = category

        # Search vector store
        results = await self.vector_store.search(
            query_vector=query_embedding,
            limit=limit,
            filter_conditions=filter_conditions if filter_conditions else None,
        )

        logger.info("Retrieved documents", query=query[:50], count=len(results))
        return results

    def build_context(self, retrieved_docs: list[dict], max_tokens: int = 4000) -> str:
        """Build context string from retrieved documents."""
        context_parts = []
        estimated_tokens = 0

        for doc in retrieved_docs:
            content = doc.get("payload", {}).get("content", "")
            title = doc.get("payload", {}).get("title", "Unknown")
            score = doc.get("score", 0)

            # Rough token estimation (1 token ≈ 4 chars)
            doc_tokens = len(content) // 4

            if estimated_tokens + doc_tokens > max_tokens:
                break

            context_parts.append(
                f"[Source: {title} (relevance: {score:.2f})]\n{content}"
            )
            estimated_tokens += doc_tokens

        return "\n\n---\n\n".join(context_parts)

    async def query(
        self,
        question: str,
        limit: int = 5,
        category: Optional[str] = None,
    ) -> dict:
        """
        Perform RAG query: retrieve context and prepare for LLM.

        Returns context and metadata for use by agent system.
        """
        retrieved_docs = await self.retrieve(
            query=question,
            limit=limit,
            category=category,
        )

        context = self.build_context(retrieved_docs)

        sources = [
            {
                "title": doc.get("payload", {}).get("title", "Unknown"),
                "source_path": doc.get("payload", {}).get("source_path", ""),
                "score": doc.get("score", 0),
            }
            for doc in retrieved_docs
        ]

        return {
            "context": context,
            "sources": sources,
            "retrieved_count": len(retrieved_docs),
        }
