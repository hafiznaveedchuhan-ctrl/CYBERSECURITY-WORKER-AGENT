"""RAG Service FastAPI application."""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import structlog

from src.services.rag_service.embeddings import EmbeddingsService
from src.services.rag_service.retriever import ContextAwareRetriever

logger = structlog.get_logger()


class RetrieveRequest(BaseModel):
    """Request for document retrieval."""
    query: str = Field(..., min_length=1, max_length=2000)
    collection: str = Field(default="textbook_chunks")
    top_k: int = Field(default=5, ge=1, le=20)
    page_filter: Optional[str] = Field(default=None, description="Filter by page/module")
    score_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    selected_text: Optional[str] = Field(default=None, description="User-selected text for context")


class RetrievedChunk(BaseModel):
    """A retrieved document chunk."""
    id: str
    content: str
    metadata: dict
    score: float
    citation: str


class RetrieveResponse(BaseModel):
    """Response from retrieval."""
    chunks: list[RetrievedChunk]
    query: str
    total_found: int


# Global services
embeddings_service: Optional[EmbeddingsService] = None
retriever: Optional[ContextAwareRetriever] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global embeddings_service, retriever

    logger.info("Starting RAG service")

    # Initialize services
    embeddings_service = EmbeddingsService()
    retriever = ContextAwareRetriever(embeddings_service)
    await retriever.initialize()

    yield

    logger.info("Shutting down RAG service")


app = FastAPI(
    title="RAG Service",
    description="Retrieval-Augmented Generation service for AI-SOC Platform",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "rag-service"}


@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_documents(request: RetrieveRequest) -> RetrieveResponse:
    """
    Retrieve relevant documents for a query.

    Supports:
    - Context-aware retrieval with selected text prioritization
    - Page/module filtering for textbook content
    - Score threshold filtering
    """
    if not retriever:
        raise HTTPException(status_code=503, detail="Retriever not initialized")

    try:
        # Build query with selected text context
        query = request.query
        if request.selected_text:
            query = f"Context: {request.selected_text}\n\nQuestion: {request.query}"

        # Perform retrieval
        results = await retriever.retrieve(
            query=query,
            collection=request.collection,
            top_k=request.top_k,
            page_filter=request.page_filter,
            score_threshold=request.score_threshold,
        )

        chunks = [
            RetrievedChunk(
                id=r["id"],
                content=r["content"],
                metadata=r["metadata"],
                score=r["score"],
                citation=r["citation"],
            )
            for r in results
        ]

        logger.info(
            "Documents retrieved",
            query_length=len(query),
            results_count=len(chunks),
            collection=request.collection,
        )

        return RetrieveResponse(
            chunks=chunks,
            query=request.query,
            total_found=len(chunks),
        )

    except Exception as e:
        logger.error("Retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")


@app.post("/embed")
async def generate_embedding(text: str) -> dict:
    """Generate embedding for text."""
    if not embeddings_service:
        raise HTTPException(status_code=503, detail="Embeddings service not initialized")

    try:
        embedding = await embeddings_service.embed_text(text)
        return {"embedding": embedding, "dimension": len(embedding)}
    except Exception as e:
        logger.error("Embedding generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
