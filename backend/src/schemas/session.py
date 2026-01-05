"""Session Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionResponse(BaseModel):
    """Session response schema."""

    id: int
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime
    created_at: datetime
    is_current: bool = False

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """Session list response schema."""

    sessions: list[SessionResponse]
    total: int
