"""
JWT Authentication & Security Module

Provides token-based authentication for protected endpoints.
Public endpoints (chat, shared conversations) don't require auth.
Admin endpoints (ingest-cv, delete) require valid API key or JWT token.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Header
import logging

logger = logging.getLogger(__name__)

# Load from environment or use default for development
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
API_KEY = os.getenv("API_KEY", None)
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


class TokenData:
    """Token payload structure"""
    def __init__(self, sub: str, exp: datetime, type: str = "access"):
        self.sub = sub
        self.exp = exp
        self.type = type


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Payload to encode
        expires_delta: Custom expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create token"
        )


def verify_token(token: str) -> dict:
    """
    Verify JWT token and return payload
    
    Args:
        token: JWT token to verify
    
    Returns:
        Token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_api_key_or_token(
    authorization: str = Header(None),
) -> str:
    """
    Verify either API key or JWT token from Authorization header
    
    Args:
        authorization: Authorization header value (format: "Bearer <token>")
    
    Returns:
        Subject (user identifier) from token/key
    
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if it's an API key
    if API_KEY and token == API_KEY:
        logger.info("Request authenticated via API key")
        return "api_key"
    
    # Otherwise verify as JWT
    try:
        payload = verify_token(token)
        sub: Optional[str] = payload.get("sub")
        
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        
        logger.info(f"Request authenticated: {sub}")
        return sub
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_jwt_token(
    authorization: str = Header(None),
) -> str:
    """
    Verify JWT token only (stricter than verify_api_key_or_token)
    
    Args:
        authorization: Authorization header value (format: "Bearer <token>")
    
    Returns:
        Subject from token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    
    payload = verify_token(token)  # This raises HTTPException if invalid
    sub = payload.get("sub", "unknown")
    return str(sub) if sub else "unknown"


def verify_optional_token(authorization: Optional[str] = None) -> Optional[str]:
    """
    Optionally verify token if provided in Authorization header
    
    Args:
        authorization: Authorization header value
    
    Returns:
        Subject if token provided and valid, None otherwise
    """
    if not authorization:
        return None
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        
        payload = verify_token(token)
        return payload.get("sub")
    
    except Exception:
        return None
