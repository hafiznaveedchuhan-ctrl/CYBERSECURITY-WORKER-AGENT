"""Database session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

# Create async engine
# Convert sslmode to ssl for asyncpg compatibility
db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
db_url = db_url.replace("sslmode=", "ssl=")
# Remove channel_binding parameter as asyncpg doesn't support it
if "channel_binding=" in db_url:
    import re
    db_url = re.sub(r"[&?]channel_binding=[^&]*", "", db_url)

engine = create_async_engine(
    db_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
