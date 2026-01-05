"""Approval request Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApprovalRequestCreate(BaseModel):
    """Approval request creation schema."""

    action_type: str
    action_description: str
    risk_level: str = Field(..., pattern="^(low|medium|high|critical)$")
    expires_in_minutes: int = Field(default=30, ge=5, le=1440)


class ApprovalDecision(BaseModel):
    """Approval decision schema."""

    approved: bool
    notes: Optional[str] = None


class ApprovalRequestResponse(BaseModel):
    """Approval request response schema."""

    id: int
    agent_run_id: int
    action_type: str
    action_description: str
    risk_level: str
    status: str
    expires_at: datetime
    created_at: datetime
    decided_at: Optional[datetime] = None
    approval_notes: Optional[str] = None
    approved_by_id: Optional[int] = None

    class Config:
        from_attributes = True


class PendingApprovalsResponse(BaseModel):
    """Pending approvals list response schema."""

    approvals: list[ApprovalRequestResponse]
    total: int
