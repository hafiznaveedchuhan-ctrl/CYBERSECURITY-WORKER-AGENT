"""Audit log Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuditLogCreate(BaseModel):
    """Audit log creation schema."""

    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogResponse(BaseModel):
    """Audit log response schema."""

    id: int
    user_id: Optional[int] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[dict] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Audit log list response schema."""

    logs: list[AuditLogResponse]
    total: int
    page: int
    page_size: int
