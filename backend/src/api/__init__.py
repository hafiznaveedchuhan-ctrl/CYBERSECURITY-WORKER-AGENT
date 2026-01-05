"""API routes module."""

from fastapi import APIRouter

from src.api.routes import auth, chat, health, documents, conversations, approvals, agent_runs

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
api_router.include_router(agent_runs.router, prefix="/agent-runs", tags=["agent-runs"])
