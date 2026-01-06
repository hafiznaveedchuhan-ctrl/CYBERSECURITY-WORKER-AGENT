"""Chat API routes with RAG and OpenAI integration."""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
import structlog

from src.config import settings
from src.services.rag import RAGService
from src.services.embedding import EmbeddingService
from src.services.vector_store import VectorStoreService
from src.auth.deps import get_current_user_optional
from src.models.user import User

router = APIRouter()
logger = structlog.get_logger()

# In-memory conversation store (replace with database in production)
conversation_store: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str = Field(..., min_length=1, max_length=10000)
    session_id: Optional[str] = Field(default=None)
    agent_type: Optional[str] = Field(default=None)


class ChatResponse(BaseModel):
    """Chat response model."""

    message: str
    session_id: str
    agent_type: str
    sources: list[dict] = Field(default_factory=list)


class ConversationHistory(BaseModel):
    """Conversation history response."""

    session_id: str
    messages: list[dict]


def get_rag_service() -> RAGService:
    """Get RAG service instance."""
    embedding_service = EmbeddingService()
    vector_store = VectorStoreService()
    return RAGService(vector_store=vector_store, embedding_service=embedding_service)


def get_openai_client() -> AsyncOpenAI:
    """Get OpenAI client."""
    return AsyncOpenAI(api_key=settings.openai_api_key)


SYSTEM_PROMPT = """You are an AI-SOC (Security Operations Center) assistant. You help security professionals with:
- Alert triage and classification
- Threat intelligence analysis
- Incident response guidance
- Detection engineering (Sigma, YARA rules)
- Security best practices

When answering questions:
1. Use the provided context from the knowledge base when available
2. Be specific and actionable in your recommendations
3. Cite sources when using context from the knowledge base
4. If you don't have enough context, provide general best practices
5. Always prioritize security and safety

You have access to these specialized capabilities:
- TRIAGE: Alert classification and severity assessment
- ENRICHMENT: IOC reputation and context gathering
- THREATINTEL: MITRE ATT&CK mapping and threat analysis
- DETECTION: Sigma and YARA rule generation
- INCIDENT-COMMANDER: Response coordination
- REPORT-WRITER: Incident report generation

Context from knowledge base:
{context}

If no relevant context is found, you can still answer general security questions using your training knowledge."""


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> ChatResponse:
    """
    Process a chat message and return AI response.

    Uses RAG to retrieve relevant context from the textbook
    and generates response using OpenAI.
    """
    session_id = request.session_id or str(uuid4())

    try:
        # Initialize services
        rag_service = get_rag_service()
        openai_client = get_openai_client()

        # Retrieve relevant context from vector store
        rag_result = await rag_service.query(
            question=request.message,
            limit=5,
        )

        context = rag_result.get("context", "")
        sources = rag_result.get("sources", [])

        # Get conversation history
        history = conversation_store.get(session_id, [])

        # Build messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(context=context if context else "No specific context found in knowledge base.")
            }
        ]

        # Add conversation history (last 10 messages)
        for msg in history[-10:]:
            messages.append(msg)

        # Add current user message
        messages.append({"role": "user", "content": request.message})

        # Generate response using OpenAI
        response = await openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            max_tokens=2000,
            temperature=0.7,
        )

        assistant_message = response.choices[0].message.content

        # Update conversation history
        if session_id not in conversation_store:
            conversation_store[session_id] = []

        conversation_store[session_id].append({"role": "user", "content": request.message})
        conversation_store[session_id].append({"role": "assistant", "content": assistant_message})

        # Determine agent type based on query content
        agent_type = determine_agent_type(request.message)

        logger.info(
            "Chat response generated",
            session_id=session_id,
            user_id=current_user.id if current_user else None,
            sources_count=len(sources),
            agent_type=agent_type,
        )

        return ChatResponse(
            message=assistant_message,
            session_id=session_id,
            agent_type=request.agent_type or agent_type,
            sources=sources,
        )

    except Exception as e:
        logger.error("Chat error", error=str(e), session_id=session_id)

        # Fallback response
        return ChatResponse(
            message=f"I apologize, but I encountered an error processing your request. Please try again. Error: {str(e)}",
            session_id=session_id,
            agent_type="supervisor",
            sources=[],
        )


def determine_agent_type(message: str) -> str:
    """Determine the appropriate agent type based on message content."""
    message_lower = message.lower()

    # Check for specific keywords to route to appropriate agent
    if any(word in message_lower for word in ["alert", "triage", "severity", "classify", "prioritize"]):
        return "triage"
    elif any(word in message_lower for word in ["ioc", "indicator", "hash", "ip address", "domain", "reputation"]):
        return "enrichment"
    elif any(word in message_lower for word in ["mitre", "att&ck", "technique", "tactic", "threat actor", "apt"]):
        return "threatintel"
    elif any(word in message_lower for word in ["sigma", "yara", "detection", "rule", "query"]):
        return "detection"
    elif any(word in message_lower for word in ["incident", "response", "containment", "eradication", "coordinate"]):
        return "incident-commander"
    elif any(word in message_lower for word in ["report", "summary", "document", "write up"]):
        return "report-writer"
    else:
        return "supervisor"


@router.get("/sessions/{session_id}", response_model=ConversationHistory)
async def get_session(
    session_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> ConversationHistory:
    """Get conversation history for a session."""
    history = conversation_store.get(session_id, [])
    return ConversationHistory(
        session_id=session_id,
        messages=history,
    )


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> dict:
    """Delete a conversation session."""
    if session_id in conversation_store:
        del conversation_store[session_id]
        return {"status": "deleted", "session_id": session_id}
    return {"status": "not_found", "session_id": session_id}


@router.get("/sessions")
async def list_sessions(
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> dict:
    """List all active sessions."""
    sessions = [
        {
            "session_id": sid,
            "message_count": len(messages),
            "last_message": messages[-1]["content"][:100] if messages else None,
        }
        for sid, messages in conversation_store.items()
    ]
    return {"sessions": sessions, "total": len(sessions)}
