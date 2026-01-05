"""Approval routes for human-in-the-loop actions."""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import structlog

from src.db import get_db
from src.models import ApprovalRequest, User, AuditLog
from src.models.agent import ApprovalStatus
from src.schemas.approval import ApprovalRequestResponse, ApprovalDecision, PendingApprovalsResponse
from src.auth.deps import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", response_model=PendingApprovalsResponse)
async def list_pending_approvals(
    status_filter: Optional[str] = Query(default="pending", regex="^(pending|approved|rejected|expired|all)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PendingApprovalsResponse:
    """List approval requests."""
    query = select(ApprovalRequest)

    if status_filter != "all":
        query = query.where(ApprovalRequest.status == status_filter)

    # Check for expired approvals and update them
    now = datetime.now(timezone.utc)
    await db.execute(
        update(ApprovalRequest)
        .where(
            ApprovalRequest.status == ApprovalStatus.PENDING.value,
            ApprovalRequest.expires_at < now,
        )
        .values(status=ApprovalStatus.EXPIRED.value)
    )

    result = await db.execute(
        query.order_by(ApprovalRequest.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    approvals = result.scalars().all()

    return PendingApprovalsResponse(
        approvals=[ApprovalRequestResponse.model_validate(a) for a in approvals],
        total=len(approvals),
    )


@router.get("/{approval_id}", response_model=ApprovalRequestResponse)
async def get_approval(
    approval_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ApprovalRequestResponse:
    """Get a specific approval request."""
    result = await db.execute(
        select(ApprovalRequest).where(ApprovalRequest.id == approval_id)
    )
    approval = result.scalar_one_or_none()

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found",
        )

    return ApprovalRequestResponse.model_validate(approval)


@router.post("/{approval_id}/approve", response_model=ApprovalRequestResponse)
async def approve_action(
    approval_id: int,
    decision: ApprovalDecision,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ApprovalRequestResponse:
    """Approve a pending action."""
    result = await db.execute(
        select(ApprovalRequest).where(ApprovalRequest.id == approval_id)
    )
    approval = result.scalar_one_or_none()

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found",
        )

    if approval.status != ApprovalStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Approval request is already {approval.status}",
        )

    if approval.expires_at < datetime.now(timezone.utc):
        approval.status = ApprovalStatus.EXPIRED.value
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Approval request has expired",
        )

    # Update approval
    approval.status = ApprovalStatus.APPROVED.value
    approval.approved_by_id = current_user.id
    approval.approval_notes = decision.notes
    approval.decided_at = datetime.now(timezone.utc)

    # Audit log
    audit = AuditLog(
        user_id=current_user.id,
        action="approve_action",
        resource_type="approval_request",
        resource_id=str(approval_id),
        details={
            "action_type": approval.action_type,
            "notes": decision.notes,
        },
    )
    db.add(audit)

    await db.commit()
    await db.refresh(approval)

    logger.info(
        "Action approved",
        approval_id=approval_id,
        approved_by=current_user.id,
        action_type=approval.action_type,
    )

    return ApprovalRequestResponse.model_validate(approval)


@router.post("/{approval_id}/reject", response_model=ApprovalRequestResponse)
async def reject_action(
    approval_id: int,
    decision: ApprovalDecision,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ApprovalRequestResponse:
    """Reject a pending action."""
    result = await db.execute(
        select(ApprovalRequest).where(ApprovalRequest.id == approval_id)
    )
    approval = result.scalar_one_or_none()

    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found",
        )

    if approval.status != ApprovalStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Approval request is already {approval.status}",
        )

    # Update approval
    approval.status = ApprovalStatus.REJECTED.value
    approval.approved_by_id = current_user.id
    approval.approval_notes = decision.notes
    approval.decided_at = datetime.now(timezone.utc)

    # Audit log
    audit = AuditLog(
        user_id=current_user.id,
        action="reject_action",
        resource_type="approval_request",
        resource_id=str(approval_id),
        details={
            "action_type": approval.action_type,
            "notes": decision.notes,
        },
    )
    db.add(audit)

    await db.commit()
    await db.refresh(approval)

    logger.info(
        "Action rejected",
        approval_id=approval_id,
        rejected_by=current_user.id,
        action_type=approval.action_type,
    )

    return ApprovalRequestResponse.model_validate(approval)
