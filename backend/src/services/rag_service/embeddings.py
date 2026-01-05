"""OpenAI embeddings wrapper."""

from typing import Optional
import asyncio

from openai import AsyncOpenAI
import structlog

from src.config import settings

logger = structlog.get_logger()


class EmbeddingsService:
    """Service for generating text embeddings using OpenAI."""

    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Initialize embeddings service.

        Args:
            model: OpenAI embedding model to use
        """
        self.model = model
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.dimension = 1536  # Default for text-embedding-3-small

    async def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("Embedding generation failed", error=str(e), text_length=len(text))
            raise

    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            batch_size: Maximum texts per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                response = await self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                )
                batch_embeddings = [d.embedding for d in response.data]
                all_embeddings.extend(batch_embeddings)

                logger.debug(
                    "Batch embeddings generated",
                    batch_num=i // batch_size + 1,
                    batch_size=len(batch),
                )

            except Exception as e:
                logger.error(
                    "Batch embedding failed",
                    error=str(e),
                    batch_start=i,
                    batch_size=len(batch),
                )
                raise

        return all_embeddings

    async def embed_with_retry(
        self,
        text: str,
        max_retries: int = 3,
        base_delay: float = 1.0,
    ) -> list[float]:
        """
        Generate embedding with exponential backoff retry.

        Args:
            text: Text to embed
            max_retries: Maximum retry attempts
            base_delay: Base delay between retries (seconds)

        Returns:
            Embedding vector
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                return await self.embed_text(text)
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        "Embedding retry",
                        attempt=attempt + 1,
                        delay=delay,
                        error=str(e),
                    )
                    await asyncio.sleep(delay)

        raise last_error
