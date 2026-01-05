"""Conversation and chat history routes."""

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
import structlog

from src.db import get_db
from src.models import Conversation, Message, User
from src.schemas.chat import ConversationResponse, MessageResponse, ConversationDetailResponse
from src.auth.deps import get_current_active_user

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", response_model=list[ConversationResponse])
async def list_conversations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> list[ConversationResponse]:
    """List user's conversations."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == str(current_user.id))
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    conversations = result.scalars().all()

    # Get message counts
    responses = []
    for conv in conversations:
        count_result = await db.execute(
            select(func.count(Message.id)).where(Message.conversation_id == conv.id)
        )
        message_count = count_result.scalar() or 0

        responses.append(
            ConversationResponse(
                id=conv.id,
                session_id=conv.session_id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=message_count,
            )
        )

    return responses


@router.get("/{session_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ConversationDetailResponse:
    """Get conversation with messages."""
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(
            Conversation.session_id == session_id,
            Conversation.user_id == str(current_user.id),
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationDetailResponse(
        id=conversation.id,
        session_id=conversation.session_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=len(conversation.messages),
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                agent_type=msg.agent_type,
                tokens_used=msg.tokens_used,
                created_at=msg.created_at,
            )
            for msg in conversation.messages
        ],
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a conversation and all its messages."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.session_id == session_id,
            Conversation.user_id == str(current_user.id),
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    await db.delete(conversation)
    await db.commit()

    logger.info("Conversation deleted", session_id=session_id, user_id=current_user.id)


@router.post("/{session_id}/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_conversation(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Clear all messages from a conversation."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.session_id == session_id,
            Conversation.user_id == str(current_user.id),
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    await db.execute(
        delete(Message).where(Message.conversation_id == conversation.id)
    )
    await db.commit()

    logger.info("Conversation cleared", session_id=session_id, user_id=current_user.id)


@router.patch("/{session_id}/title")
async def update_conversation_title(
    session_id: str,
    title: str = Query(..., min_length=1, max_length=255),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> ConversationResponse:
    """Update conversation title."""
    result = await db.execute(
        select(Conversation).where(
            Conversation.session_id == session_id,
            Conversation.user_id == str(current_user.id),
        )
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    conversation.title = title
    await db.commit()
    await db.refresh(conversation)

    count_result = await db.execute(
        select(func.count(Message.id)).where(Message.conversation_id == conversation.id)
    )
    message_count = count_result.scalar() or 0

    return ConversationResponse(
        id=conversation.id,
        session_id=conversation.session_id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=message_count,
    )
