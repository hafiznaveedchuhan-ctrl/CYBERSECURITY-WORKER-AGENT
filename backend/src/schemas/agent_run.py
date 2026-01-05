"""Agent run Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AgentRunCreate(BaseModel):
    """Agent run creation schema."""

    conversation_id: int
    agent_type: str
    input_message: str
    context_used: Optional[dict] = None


class AgentRunUpdate(BaseModel):
    """Agent run update schema."""

    status: Optional[str] = None
    output_message: Optional[str] = None
    tools_called: Optional[list] = None
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    latency_ms: Optional[int] = None
    error_message: Optional[str] = None


class AgentRunResponse(BaseModel):
    """Agent run response schema."""

    id: int
    conversation_id: int
    agent_type: str
    status: str
    input_message: str
    output_message: Optional[str] = None
    tools_called: Optional[list] = None
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    latency_ms: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AgentRunListResponse(BaseModel):
    """Agent run list response schema."""

    runs: list[AgentRunResponse]
    total: int
