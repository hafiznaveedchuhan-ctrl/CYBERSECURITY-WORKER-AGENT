"""Password hashing and verification."""

from passlib.context import CryptContext

# Use bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Truncate password to 72 bytes to handle bcrypt 4.2.x compatibility.
    """
    # bcrypt only uses first 72 bytes, truncate to avoid errors
    truncated = password[:72]
    return pwd_context.hash(truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)
