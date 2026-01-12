"""AI SOC Backend - Main FastAPI Application."""

import subprocess
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from src.config import settings
from src.api import api_router
from src.api.middleware import RequestIdMiddleware, TimingMiddleware, RateLimitMiddleware

logger = structlog.get_logger()


def run_migrations():
    """Run database migrations on startup."""
    import os
    # Get the backend directory (parent of src)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        logger.info("Running database migrations...", cwd=backend_dir)
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True,
            cwd=backend_dir
        )
        logger.info("Migrations completed", output=result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Migration failed", error=e.stderr, stdout=e.stdout)
    except Exception as e:
        logger.error("Migration error", error=str(e))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup and shutdown events."""
    # Startup - run migrations first
    run_migrations()
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
