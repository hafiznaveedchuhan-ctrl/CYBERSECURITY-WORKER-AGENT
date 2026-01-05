"""Document API routes."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


class DocumentResponse(BaseModel):
    """Document response model."""

    id: int
    title: str
    source_path: str
    category: Optional[str]
    chunk_count: int


class SearchRequest(BaseModel):
    """Search request model."""

    query: str = Field(..., min_length=1, max_length=1000)
    limit: int = Field(default=5, ge=1, le=20)
    category: Optional[str] = Field(default=None)


class SearchResult(BaseModel):
    """Search result model."""

    content: str
    document_title: str
    score: float
    metadata: dict = Field(default_factory=dict)


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    category: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[DocumentResponse]:
    """List all indexed documents."""
    # TODO: Implement document listing from database
    return []


@router.post("/search", response_model=list[SearchResult])
async def search_documents(request: SearchRequest) -> list[SearchResult]:
    """
    Semantic search across indexed documents.

    Uses Qdrant vector similarity search to find relevant content.
    """
    # TODO: Implement vector search via Qdrant
    return []


@router.post("/ingest")
async def ingest_documents() -> dict:
    """
    Trigger document ingestion from the docs folder.

    Processes markdown files, chunks them, generates embeddings,
    and stores in Qdrant.
    """
    # TODO: Implement document ingestion pipeline
    return {
        "status": "ingestion_started",
        "message": "Document ingestion is being implemented",
    }
