"""Base agent class for all AI sub-agents."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from openai import AsyncOpenAI
from pydantic import BaseModel
import structlog

from src.config import settings

logger = structlog.get_logger()


class AgentMessage(BaseModel):
    """Message structure for agent communication."""

    role: str
    content: str
    agent_type: Optional[str] = None
    metadata: dict = {}


class AgentResponse(BaseModel):
    """Response structure from agents."""

    content: str
    agent_type: str
    confidence: float = 1.0
    sources: list[dict] = []
    tool_calls: list[dict] = []
    metadata: dict = {}


class BaseAgent(ABC):
    """Base class for all AI sub-agents."""

    agent_type: str = "base"
    description: str = "Base agent"
    system_prompt: str = "You are a helpful AI assistant."

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        self.client = AsyncOpenAI(api_key=self.api_key)

    @abstractmethod
    async def process(
        self,
        message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> AgentResponse:
        """Process a message and return response."""
        pass

    async def _call_llm(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Call OpenAI API with messages."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content or ""
        logger.info(
            "LLM response generated",
            agent=self.agent_type,
            tokens=response.usage.total_tokens if response.usage else 0,
        )
        return content

    def _build_messages(
        self,
        user_message: str,
        context: Optional[str] = None,
        conversation_history: Optional[list[AgentMessage]] = None,
    ) -> list[dict]:
        """Build message list for LLM call."""
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages
                messages.append({"role": msg.role, "content": msg.content})

        # Add context if available
        if context:
            messages.append({
                "role": "system",
                "content": f"Relevant context from the SOC textbook:\n\n{context}",
            })

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages
