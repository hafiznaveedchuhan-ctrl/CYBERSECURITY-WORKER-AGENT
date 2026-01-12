"""AI SOC Backend - Main FastAPI Application."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from src.config import settings
from src.api import api_router
from src.api.middleware import RequestIdMiddleware, TimingMiddleware, RateLimitMiddleware

# Import all models FIRST to ensure they are registered with Base metadata
# This must happen before any database operations
from src.models import (
    User, Session, AuditLog,
    Conversation, Message,
    Document, DocumentChunk,
    AgentRun, ApprovalRequest
)

logger = structlog.get_logger()


async def create_tables():
    """Create database tables on startup."""
    from src.db import engine
    from src.db.base import Base

    try:
        logger.info("Creating database tables...",
                    tables=list(Base.metadata.tables.keys()))
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully",
                    tables=list(Base.metadata.tables.keys()))
    except Exception as e:
        logger.error("Failed to create tables",
                     error=str(e),
                     traceback=traceback.format_exc())
        # Re-raise to prevent silent failures
        raise


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup and shutdown events."""
    # Startup - create tables first
    try:
        await create_tables()
    except Exception as e:
        # Log but continue - migrations may have already created tables
        logger.warning("Table creation error (may be OK if migrations ran)",
                       error=str(e))
    logger.info("Starting AI SOC Backend", version=settings.app_version)
    yield
    # Shutdown
    logger.info("Shutting down AI SOC Backend")


app = FastAPI(
    title="AI SOC Backend",
    description="AI-powered Security Operations Center API",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add middleware (order matters - first added is outermost)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.rate_limit_per_minute)
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Configure CORS - Allow all origins for now (can be restricted later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "AI SOC Backend API", "version": settings.app_version}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
