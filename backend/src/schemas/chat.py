"""Chat Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request schema."""

    message: str = Field(..., min_length=1, max_length=10000)
    session_id: Optional[str] = None
    agent_type: Optional[str] = None
    context_filter: Optional[dict] = None  # For filtering RAG context


class SourceReference(BaseModel):
    """Source reference in chat response."""

    title: str
    source_path: str
    score: float
    snippet: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema."""

    message: str
    session_id: str
    agent_type: str
    sources: list[SourceReference] = Field(default_factory=list)
    tokens_used: Optional[int] = None
    latency_ms: Optional[int] = None


class MessageResponse(BaseModel):
    """Message response schema."""

    id: int
    role: str
    content: str
    agent_type: Optional[str] = None
    tokens_used: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Conversation response schema."""

    id: int
    session_id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True


class ConversationDetailResponse(ConversationResponse):
    """Conversation with messages response schema."""

    messages: list[MessageResponse] = Field(default_factory=list)
