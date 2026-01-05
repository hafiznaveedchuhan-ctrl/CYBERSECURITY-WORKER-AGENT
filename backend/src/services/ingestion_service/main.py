"""Ingestion Service FastAPI application."""

from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import structlog

from src.services.ingestion_service.chunker import MarkdownChunker
from src.services.ingestion_service.indexer import QdrantIndexer

logger = structlog.get_logger()


class JobStatus(str, Enum):
    """Ingestion job status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class IngestTextbookRequest(BaseModel):
    """Request to ingest textbook content."""
    content: str = Field(..., min_length=1)
    module: str = Field(..., description="Module identifier (e.g., module-1-soc-foundations)")
    section: Optional[str] = Field(default=None)
    source_path: Optional[str] = Field(default=None)


class IngestJob(BaseModel):
    """Ingestion job status."""
    id: str
    status: JobStatus
    module: str
    chunks_processed: int = 0
    total_chunks: int = 0
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class IngestResponse(BaseModel):
    """Response from ingestion request."""
    job_id: str
    status: JobStatus
    message: str


# In-memory job storage (use Redis in production)
jobs: dict[str, IngestJob] = {}

# Global services
chunker: Optional[MarkdownChunker] = None
indexer: Optional[QdrantIndexer] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global chunker, indexer

    logger.info("Starting Ingestion service")

    # Initialize services
    chunker = MarkdownChunker()
    indexer = QdrantIndexer()
    await indexer.initialize()

    yield

    if indexer:
        await indexer.close()
    logger.info("Shutting down Ingestion service")


app = FastAPI(
    title="Ingestion Service",
    description="Document ingestion service for AI-SOC Platform",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ingestion-service"}


async def process_ingestion(job_id: str, content: str, module: str, section: Optional[str]):
    """Background task to process document ingestion."""
    job = jobs.get(job_id)
    if not job:
        return

    try:
        job.status = JobStatus.PROCESSING

        # Chunk the content
        chunks = chunker.chunk_markdown(
            content=content,
            module=module,
            section=section,
        )

        job.total_chunks = len(chunks)

        # Index chunks
        for i, chunk in enumerate(chunks):
            await indexer.index_chunk(chunk)
            job.chunks_processed = i + 1

        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()

        logger.info(
            "Ingestion completed",
            job_id=job_id,
            chunks=len(chunks),
            module=module,
        )

    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)
        job.completed_at = datetime.utcnow()

        logger.error(
            "Ingestion failed",
            job_id=job_id,
            error=str(e),
        )


@app.post("/ingest/textbook", response_model=IngestResponse)
async def ingest_textbook(
    request: IngestTextbookRequest,
    background_tasks: BackgroundTasks,
) -> IngestResponse:
    """
    Ingest textbook content into the vector store.

    Chunks the markdown content and indexes it in Qdrant
    for RAG retrieval.
    """
    job_id = str(uuid4())

    # Create job
    job = IngestJob(
        id=job_id,
        status=JobStatus.PENDING,
        module=request.module,
        created_at=datetime.utcnow(),
    )
    jobs[job_id] = job

    # Start background processing
    background_tasks.add_task(
        process_ingestion,
        job_id,
        request.content,
        request.module,
        request.section,
    )

    logger.info(
        "Ingestion job created",
        job_id=job_id,
        module=request.module,
        content_length=len(request.content),
    )

    return IngestResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        message="Ingestion job created",
    )


@app.get("/ingest/jobs/{job_id}", response_model=IngestJob)
async def get_job_status(job_id: str) -> IngestJob:
    """Get the status of an ingestion job."""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/ingest/jobs", response_model=list[IngestJob])
async def list_jobs(
    status: Optional[JobStatus] = None,
    limit: int = 20,
) -> list[IngestJob]:
    """List ingestion jobs."""
    job_list = list(jobs.values())

    if status:
        job_list = [j for j in job_list if j.status == status]

    # Sort by created_at desc
    job_list.sort(key=lambda x: x.created_at, reverse=True)

    return job_list[:limit]


@app.delete("/ingest/jobs/{job_id}")
async def delete_job(job_id: str) -> dict:
    """Delete a completed or failed job."""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status in [JobStatus.PENDING, JobStatus.PROCESSING]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete job in progress",
        )

    del jobs[job_id]
    return {"message": "Job deleted", "job_id": job_id}
