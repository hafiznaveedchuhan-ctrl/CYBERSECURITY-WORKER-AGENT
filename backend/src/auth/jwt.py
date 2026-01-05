"""JWT token generation and validation."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4
import hashlib

from jose import JWTError, jwt
from pydantic import ValidationError
import structlog

from src.config import settings
from src.schemas.user import TokenPayload

logger = structlog.get_logger()

ALGORITHM = "HS256"


def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, str]:
    """
    Create an access token for a user.

    Returns:
        tuple: (token, token_id for revocation tracking)
    """
    now = datetime.now(timezone.utc)
    token_id = str(uuid4())

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.jwt_expire_minutes)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": now,
        "jti": token_id,
        "type": "access",
    }

    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)
    return token, token_id


def create_refresh_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, str]:
    """
    Create a refresh token for a user.

    Returns:
        tuple: (token, token_id for revocation tracking)
    """
    now = datetime.now(timezone.utc)
    token_id = str(uuid4())

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=7)  # Refresh tokens last 7 days

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": now,
        "jti": token_id,
        "type": "refresh",
    }

    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)
    return token, token_id


def verify_token(token: str, expected_type: str = "access") -> Optional[TokenPayload]:
    """
    Verify a JWT token and return the payload.

    Args:
        token: The JWT token to verify
        expected_type: Expected token type (access or refresh)

    Returns:
        TokenPayload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
        )

        # Validate payload structure
        token_data = TokenPayload(
            sub=payload["sub"],
            exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            iat=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
            jti=payload["jti"],
            type=payload["type"],
        )

        # Verify token type
        if token_data.type != expected_type:
            logger.warning("Token type mismatch", expected=expected_type, got=token_data.type)
            return None

        return token_data

    except JWTError as e:
        logger.warning("JWT verification failed", error=str(e))
        return None
    except ValidationError as e:
        logger.warning("Token payload validation failed", error=str(e))
        return None


def hash_token(token: str) -> str:
    """Hash a token for storage (used for revocation tracking)."""
    return hashlib.sha256(token.encode()).hexdigest()
