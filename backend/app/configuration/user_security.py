"""
Authentication and user security utilities.
Handles password hashing, JWT token creation, and user verification.
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
import bcrypt

from backend.app.configuration.app_config import config


def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt directly."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hash using bcrypt directly."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=config.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.jwt_algorithm)


def create_refresh_token(data: dict) -> str:
    """
    Creates a JWT refresh token with longer expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=config.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.jwt_algorithm)


def decode_token(token: str) -> dict:
    """
    Decodes and validates a JWT token.
    Returns the payload if valid, raises JWTError otherwise.
    """
    return jwt.decode(token, config.secret_key, algorithms=[config.jwt_algorithm])
