"""API routes module."""

from fastapi import APIRouter

from src.api.routes import chat, health, documents

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
