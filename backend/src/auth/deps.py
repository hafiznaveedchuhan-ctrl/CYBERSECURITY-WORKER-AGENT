"""Authentication dependencies for FastAPI."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from src.db import get_db
from src.models import User, Session
from src.auth.jwt import verify_token, hash_token

logger = structlog.get_logger()

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Get the current authenticated user from the JWT token.

    Returns None if no token is provided (for optional auth).
    Raises HTTPException if token is invalid.
    """
    if credentials is None:
        return None

    token = credentials.credentials

    # Verify the token
    token_data = verify_token(token, expected_type="access")
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if session is revoked
    token_hash = hash_token(token)
    session_result = await db.execute(
        select(Session).where(
            Session.token_hash == token_hash,
            Session.is_revoked == False,  # noqa: E712
        )
    )
    session = session_result.scalar_one_or_none()

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the user
    user_id = int(token_data.sub)
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user),
) -> User:
    """
    Get the current authenticated and active user.

    Raises HTTPException if user is not authenticated or not active.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    # Check if user is locked out
    if current_user.locked_until:
        from datetime import datetime, timezone

        if current_user.locked_until > datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is temporarily locked due to too many failed login attempts",
            )

    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get the current authenticated superuser.

    Raises HTTPException if user is not a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Get the current authenticated user if token is provided.

    Returns None if no token is provided or token is invalid.
    Does not raise exceptions - for optional authentication.
    """
    if credentials is None:
        return None

    token = credentials.credentials

    try:
        # Verify the token
        token_data = verify_token(token, expected_type="access")
        if token_data is None:
            return None

        # Check if session is revoked
        token_hash = hash_token(token)
        session_result = await db.execute(
            select(Session).where(
                Session.token_hash == token_hash,
                Session.is_revoked == False,  # noqa: E712
            )
        )
        session = session_result.scalar_one_or_none()

        if session is None:
            return None

        # Get the user
        user_id = int(token_data.sub)
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()

        return user
    except Exception:
        return None
