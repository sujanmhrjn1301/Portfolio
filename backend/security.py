"""
Security Utilities

Provides input validation, sanitization, rate limiting, and security headers.
"""

import re
import logging
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter (use Redis for production)"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum requests per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict = {}  # IP -> list of timestamps
    
    def is_allowed(self, client_ip: str) -> bool:
        """
        Check if request from client IP is allowed
        
        Args:
            client_ip: Client IP address
        
        Returns:
            True if request is allowed, False if rate limited
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Initialize or get request list for this IP
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Remove old requests outside the window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > window_start
        ]
        
        # Check if over limit
        if len(self.requests[client_ip]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return False
        
        # Record this request
        self.requests[client_ip].append(now)
        return True


rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


def validate_message_content(content: str, max_length: int = 10000) -> str:
    """
    Validate and sanitize message content
    
    Args:
        content: Raw message content
        max_length: Maximum allowed length
    
    Returns:
        Sanitized message content
    
    Raises:
        HTTPException: If validation fails
    """
    if not isinstance(content, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message must be a string"
        )
    
    content = content.strip()
    
    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    if len(content) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Message exceeds maximum length of {max_length} characters"
        )
    
    # Remove potentially harmful characters but allow most text
    # This is basic - adjust based on your needs
    sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', content)
    
    return sanitized


def validate_title(title: str, max_length: int = 200) -> str:
    """
    Validate and sanitize conversation title
    
    Args:
        title: Raw title
        max_length: Maximum allowed length
    
    Returns:
        Sanitized title
    
    Raises:
        HTTPException: If validation fails
    """
    if not isinstance(title, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be a string"
        )
    
    title = title.strip()
    
    if len(title) == 0:
        title = "New Chat"
    
    if len(title) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Title exceeds maximum length of {max_length}"
        )
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', title)
    
    return sanitized


def validate_conversation_id(conv_id: str) -> str:
    """
    Validate conversation ID format (UUID)
    
    Args:
        conv_id: Conversation ID
    
    Returns:
        Validated ID
    
    Raises:
        HTTPException: If format invalid
    """
    # UUID v4 format
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    if not uuid_pattern.match(conv_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )
    
    return conv_id


def validate_share_id(share_id: str) -> str:
    """
    Validate share ID format (UUID)
    
    Args:
        share_id: Share ID
    
    Returns:
        Validated ID
    
    Raises:
        HTTPException: If format invalid
    """
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    if not uuid_pattern.match(share_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid share ID format"
        )
    
    return share_id


def get_client_ip(request: Request) -> str:
    """
    Extract client IP from request, considering X-Forwarded-For header
    
    Args:
        request: FastAPI request object
    
    Returns:
        Client IP address
    """
    # Check for X-Forwarded-For header (when behind proxy)
    if "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"].split(",")[0].strip()
    
    return request.client.host if request.client else "unknown"


async def check_rate_limit(request: Request) -> bool:
    """
    Check rate limit for client
    
    Args:
        request: FastAPI request object
    
    Returns:
        True if request is allowed
    
    Raises:
        HTTPException: If rate limited
    """
    client_ip = get_client_ip(request)
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    return True


def create_secure_error_response(status_code: int, message: str) -> dict:
    """
    Create a secure error response (doesn't leak stack traces)
    
    Args:
        status_code: HTTP status code
        message: User-friendly error message
    
    Returns:
        Error response dict
    """
    # Map status codes to generic messages
    status_messages = {
        400: "Bad request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not found",
        429: "Too many requests",
        500: "Internal server error",
    }
    
    return {
        "error": status_messages.get(status_code, "Error"),
        "message": message,
        "status_code": status_code
    }


def validate_cors_origin(origin: str, allowed_origins: List[str]) -> bool:
    """
    Validate that origin is in allowed list
    
    Args:
        origin: Request origin
        allowed_origins: List of allowed origins
    
    Returns:
        True if origin is allowed
    """
    if not origin:
        return False
    
    # Exact match check (no wildcards for security)
    return origin in allowed_origins
