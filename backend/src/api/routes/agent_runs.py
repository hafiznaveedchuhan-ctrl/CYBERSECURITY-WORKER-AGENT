"""Agent run tracking routes."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import structlog

from src.db import get_db
from src.models import AgentRun, User
from src.schemas.agent_run import AgentRunResponse, AgentRunListResponse
from src.auth.deps import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", response_model=AgentRunListResponse)
async def list_agent_runs(
    agent_type: Optional[str] = Query(default=None),
    status_filter: Optional[str] = Query(default=None),
    conversation_id: Optional[int] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> AgentRunListResponse:
    """List agent runs with filters."""
    query = select(AgentRun)

    if agent_type:
        query = query.where(AgentRun.agent_type == agent_type)
    if status_filter:
        query = query.where(AgentRun.status == status_filter)
    if conversation_id:
        query = query.where(AgentRun.conversation_id == conversation_id)

    # Get total count
    count_query = select(func.count(AgentRun.id))
    if agent_type:
        count_query = count_query.where(AgentRun.agent_type == agent_type)
    if status_filter:
        count_query = count_query.where(AgentRun.status == status_filter)
    if conversation_id:
        count_query = count_query.where(AgentRun.conversation_id == conversation_id)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    result = await db.execute(
        query.order_by(AgentRun.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    runs = result.scalars().all()

    return AgentRunListResponse(
        runs=[AgentRunResponse.model_validate(r) for r in runs],
        total=total,
    )


@router.get("/{run_id}", response_model=AgentRunResponse)
async def get_agent_run(
    run_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> AgentRunResponse:
    """Get a specific agent run."""
    result = await db.execute(
        select(AgentRun).where(AgentRun.id == run_id)
    )
    run = result.scalar_one_or_none()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent run not found",
        )

    return AgentRunResponse.model_validate(run)


@router.get("/stats/summary")
async def get_agent_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get agent run statistics."""
    # Total runs by agent type
    type_result = await db.execute(
        select(AgentRun.agent_type, func.count(AgentRun.id))
        .group_by(AgentRun.agent_type)
    )
    by_type = {row[0]: row[1] for row in type_result.fetchall()}

    # Total runs by status
    status_result = await db.execute(
        select(AgentRun.status, func.count(AgentRun.id))
        .group_by(AgentRun.status)
    )
    by_status = {row[0]: row[1] for row in status_result.fetchall()}

    # Average latency
    latency_result = await db.execute(
        select(func.avg(AgentRun.latency_ms))
        .where(AgentRun.latency_ms.isnot(None))
    )
    avg_latency = latency_result.scalar() or 0

    # Total tokens
    tokens_result = await db.execute(
        select(
            func.sum(AgentRun.tokens_input),
            func.sum(AgentRun.tokens_output),
        )
    )
    tokens = tokens_result.fetchone()

    return {
        "by_agent_type": by_type,
        "by_status": by_status,
        "avg_latency_ms": round(avg_latency, 2),
        "total_tokens_input": tokens[0] or 0,
        "total_tokens_output": tokens[1] or 0,
    }
