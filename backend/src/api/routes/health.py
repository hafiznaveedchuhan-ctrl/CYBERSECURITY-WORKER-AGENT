"""Health check routes."""

from fastapi import APIRouter
from sqlalchemy import text, inspect

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    """Readiness check endpoint."""
    # TODO: Add database and Qdrant connectivity checks
    return {"status": "ready"}


@router.get("/debug/db")
async def db_debug():
    """Debug database connectivity and tables."""
    from src.db import engine
    from src.db.base import Base
    from src.models import User, Session, AuditLog

    result = {
        "connection": "unknown",
        "tables_in_metadata": list(Base.metadata.tables.keys()),
        "tables_in_db": [],
        "users_table_exists": False,
        "error": None
    }

    try:
        async with engine.connect() as conn:
            result["connection"] = "ok"

            # Check existing tables
            tables_result = await conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            )
            result["tables_in_db"] = [row[0] for row in tables_result.fetchall()]
            result["users_table_exists"] = "users" in result["tables_in_db"]

    except Exception as e:
        result["connection"] = "failed"
        result["error"] = str(e)

    return result


@router.post("/debug/create-tables")
async def create_tables_endpoint():
    """Manually trigger table creation."""
    from src.db import engine
    from src.db.base import Base
    from src.models import User, Session, AuditLog, Conversation, Message, Document, DocumentChunk, AgentRun, ApprovalRequest

    result = {
        "status": "unknown",
        "tables_created": [],
        "error": None
    }

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        result["status"] = "success"
        result["tables_created"] = list(Base.metadata.tables.keys())
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)

    return result
