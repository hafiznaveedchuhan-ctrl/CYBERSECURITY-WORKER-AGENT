"""Context-aware retriever with page filtering."""

from typing import Optional
import structlog

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from src.config import settings
from src.services.rag_service.embeddings import EmbeddingsService

logger = structlog.get_logger()


class ContextAwareRetriever:
    """Retriever with context-aware filtering and citation generation."""

    def __init__(self, embeddings_service: EmbeddingsService):
        """
        Initialize retriever.

        Args:
            embeddings_service: Service for generating embeddings
        """
        self.embeddings = embeddings_service
        self.client: Optional[AsyncQdrantClient] = None

    async def initialize(self):
        """Initialize Qdrant client."""
        self.client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
        )
        logger.info("Qdrant client initialized", url=settings.QDRANT_URL)

    async def retrieve(
        self,
        query: str,
        collection: str = "textbook_chunks",
        top_k: int = 5,
        page_filter: Optional[str] = None,
        score_threshold: float = 0.7,
    ) -> list[dict]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query
            collection: Qdrant collection name
            top_k: Number of results to return
            page_filter: Filter by page/module (e.g., "module-1")
            score_threshold: Minimum similarity score

        Returns:
            List of retrieved chunks with metadata
        """
        if not self.client:
            raise RuntimeError("Retriever not initialized")

        # Generate query embedding
        query_embedding = await self.embeddings.embed_text(query)

        # Build filter if page specified
        search_filter = None
        if page_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="module",
                        match=MatchValue(value=page_filter),
                    )
                ]
            )

        try:
            # Search Qdrant
            results = await self.client.search(
                collection_name=collection,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter,
                score_threshold=score_threshold,
            )

            # Format results
            chunks = []
            for result in results:
                metadata = result.payload or {}

                # Generate citation
                citation = self._generate_citation(metadata)

                chunks.append({
                    "id": str(result.id),
                    "content": metadata.get("content", ""),
                    "metadata": metadata,
                    "score": result.score,
                    "citation": citation,
                })

            logger.info(
                "Retrieval complete",
                query_length=len(query),
                results=len(chunks),
                collection=collection,
                page_filter=page_filter,
            )

            return chunks

        except Exception as e:
            logger.error("Retrieval failed", error=str(e), collection=collection)
            raise

    def _generate_citation(self, metadata: dict) -> str:
        """
        Generate a citation string from metadata.

        Args:
            metadata: Document metadata

        Returns:
            Formatted citation string
        """
        module = metadata.get("module", "Unknown Module")
        section = metadata.get("section", "")
        page = metadata.get("page", "")

        parts = [module]
        if section:
            parts.append(section)
        if page:
            parts.append(f"p.{page}")

        return " > ".join(parts)

    async def retrieve_with_rerank(
        self,
        query: str,
        collection: str = "textbook_chunks",
        initial_k: int = 20,
        final_k: int = 5,
        page_filter: Optional[str] = None,
    ) -> list[dict]:
        """
        Retrieve with two-stage retrieval and reranking.

        First retrieves more results, then reranks based on
        additional relevance signals.

        Args:
            query: Search query
            collection: Collection name
            initial_k: Initial retrieval count
            final_k: Final results after reranking
            page_filter: Module filter

        Returns:
            Reranked list of chunks
        """
        # Initial retrieval
        initial_results = await self.retrieve(
            query=query,
            collection=collection,
            top_k=initial_k,
            page_filter=page_filter,
            score_threshold=0.5,  # Lower threshold for initial
        )

        if len(initial_results) <= final_k:
            return initial_results

        # Simple reranking based on keyword overlap
        query_words = set(query.lower().split())

        for result in initial_results:
            content_words = set(result["content"].lower().split())
            overlap = len(query_words & content_words)
            # Boost score with keyword overlap
            result["rerank_score"] = result["score"] + (overlap * 0.1)

        # Sort by rerank score and return top_k
        initial_results.sort(key=lambda x: x["rerank_score"], reverse=True)

        return initial_results[:final_k]

    async def close(self):
        """Close Qdrant client."""
        if self.client:
            await self.client.close()
            logger.info("Qdrant client closed")
