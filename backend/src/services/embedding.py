"""Embedding service using OpenAI."""

from typing import Optional

from openai import AsyncOpenAI
import structlog

from src.config import settings

logger = structlog.get_logger()


class EmbeddingService:
    """Service for generating text embeddings using OpenAI."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_embedding_model
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        response = await self.client.embeddings.create(
            input=text,
            model=self.model,
        )
        return response.data[0].embedding

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if not texts:
            return []

        # OpenAI supports batch embedding
        response = await self.client.embeddings.create(
            input=texts,
            model=self.model,
        )

        # Sort by index to maintain order
        sorted_data = sorted(response.data, key=lambda x: x.index)
        embeddings = [item.embedding for item in sorted_data]

        logger.info("Generated embeddings", count=len(embeddings))
        return embeddings
