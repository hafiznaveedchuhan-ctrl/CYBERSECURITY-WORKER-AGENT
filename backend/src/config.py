"""AI SOC Backend - Configuration."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql://localhost:5432/ai_soc"

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "ai_soc_docs"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
