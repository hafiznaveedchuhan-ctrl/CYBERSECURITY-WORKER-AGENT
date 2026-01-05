"""Conversation and Message models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class MessageRole(str, Enum):
    """Message role enumeration."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AgentType(str, Enum):
    """AI Agent type enumeration."""

    SUPERVISOR = "supervisor"
    TRIAGE = "triage"
    ENRICHMENT = "enrichment"
    THREATINTEL = "threatintel"
    DETECTION = "detection"
    INCIDENT = "incident"
    REPORT = "report"


class Conversation(Base):
    """Conversation model for chat sessions."""

    __tablename__ = "conversations"

    title: Mapped[str] = mapped_column(String(255), nullable=True)
    session_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, nullable=True)

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(Base):
    """Message model for individual chat messages."""

    __tablename__ = "messages"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    agent_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
