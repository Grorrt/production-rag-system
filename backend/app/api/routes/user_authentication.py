"""
Authentication routes for user login and registration.
Uses JWT tokens for stateless authentication.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.app.configuration.user_security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

_in_memory_users = {}


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register")
def register(request: RegisterRequest):
    """
    Registers a new user account.
    """
    if len(request.username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters",
        )

    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    if request.username in _in_memory_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    hashed = hash_password(request.password)
    _in_memory_users[request.username] = {
        "password": hashed,
        "user_id": f"user_{len(_in_memory_users) + 1}",
    }

    return {"message": "User registered successfully", "username": request.username}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Authenticates a user and returns JWT tokens.
    """
    user = _in_memory_users.get(request.username)
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token_data = {"sub": request.username, "user_id": user["user_id"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
