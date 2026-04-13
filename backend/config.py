"""
Portfolio Configuration

Supports environment-based configuration for development/production.
Environment variables override defaults.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# ============ ENVIRONMENT ============
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ============ PORTFOLIO OWNER INFORMATION ============
# Can be customized via environment variables for multi-user deployment
PORTFOLIO_OWNER = {
    "name": os.getenv("PORTFOLIO_NAME", "Sujan Maharjan"),
    "email": os.getenv("PORTFOLIO_EMAIL", "contact@example.com"),
    # Don't expose phone/location in API - keep local only
    "phone": os.getenv("PORTFOLIO_PHONE", ""),  # Keep empty for production
    "location": os.getenv("PORTFOLIO_LOCATION", ""),  # Keep empty for production
    "github": os.getenv("PORTFOLIO_GITHUB", "https://github.com/sujanmhrjn1301"),
    "linkedin": os.getenv("PORTFOLIO_LINKEDIN", "https://linkedin.com/in/your-profile"),
}

# ============ SECURITY ============
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
API_KEY = os.getenv("API_KEY", None)  # Optional API key for admin endpoints

# ============ CORS CONFIGURATION ============
def get_cors_origins() -> List[str]:
    """
    Get CORS origins from environment or use defaults
    
    Environment variable format: comma-separated, no spaces
    Example: CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://example.com
    """
    cors_env = os.getenv("CORS_ORIGINS", "")
    
    if cors_env:
        return [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    
    # Default origins based on environment
    if ENVIRONMENT == "production":
        # Production: only specific domains
        return [
            "https://sujanmaharjan.com",  # Update with your domain
        ]
    
    # Development: localhost only
    return [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

CORS_ORIGINS = get_cors_origins()

# ============ CHAT CONFIG ============
CHAT_CONFIG = {
    "model": os.getenv("CHAT_MODEL", "openai/gpt-4o-mini"),
    "temperature": float(os.getenv("CHAT_TEMPERATURE", "0.4")),
    "max_tokens": int(os.getenv("CHAT_MAX_TOKENS", "1000")),
    "system_prompt": """You are a professional portfolio assistant for {name}.

RESPONSE GUIDELINES:
- Be direct, concise, and professional
- Use bullet points for clarity
- Include relevant links (GitHub, LinkedIn) when available
- No truncation - always complete your responses fully
- Answer to the point - don't ramble
- Use short, clear language
- Include specific evidence from the portfolio (projects, dates, achievements)
- Only provide extra details if the user explicitly asks for "more details" or "tell me more"
- Format: Lead with the main answer, then support with evidence"""
}

# ============ RAG CONFIG ============
RAG_CONFIG = {
    "chunk_size": int(os.getenv("RAG_CHUNK_SIZE", "500")),
    "chunk_overlap": int(os.getenv("RAG_CHUNK_OVERLAP", "50")),
    "distance_threshold": float(os.getenv("RAG_DISTANCE_THRESHOLD", "1.5")),
    "n_results": int(os.getenv("RAG_N_RESULTS", "5")),
    "embedding_model": os.getenv("RAG_EMBEDDING_MODEL", "text-embedding-3-small"),
    "collection_name": os.getenv("RAG_COLLECTION_NAME", "portfolio_cv"),
}

# ============ DATABASE CONFIG ============
DATABASE_CONFIG = {
    "chat_history_db": os.getenv("CHAT_DB_PATH", "./chat_history.db"),
    "chroma_db_path": os.getenv("CHROMA_DB_PATH", "./chroma_db"),
}

# ============ GITHUB INTEGRATION CONFIG ============
GITHUB_CONFIG = {
    "enabled": os.getenv("GITHUB_ENABLED", "true").lower() == "true",
    "username": os.getenv("GITHUB_USERNAME", "sujanmhrjn1301"),
    "token": os.getenv("GITHUB_TOKEN", None),  # Will be loaded from environment
    "include_readme": os.getenv("GITHUB_INCLUDE_README", "true").lower() == "true",
    "include_stars": os.getenv("GITHUB_INCLUDE_STARS", "true").lower() == "true",
    "include_languages": os.getenv("GITHUB_INCLUDE_LANGUAGES", "true").lower() == "true",
    "include_topics": os.getenv("GITHUB_INCLUDE_TOPICS", "true").lower() == "true",
}

# ============ RATE LIMITING ============
RATE_LIMIT_CONFIG = {
    "max_requests": int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
    "window_seconds": int(os.getenv("RATE_LIMIT_WINDOW", "60")),
}

# ============ UI CONFIG ============
UI_CONFIG = {
    "app_title": f"{PORTFOLIO_OWNER['name']} - Portfolio",
    "app_description": "An AI-powered portfolio where you can chat with me about my experience, skills, and projects.",
    "colors": {
        "dark_gray": "#1a1a1a",
        "medium_gray": "#2d2d30",
        "light_gray": "#3e3e42",
        "lighter_gray": "#ececf1",
        "blue_accent": "#3b82f6",
    },
    "quick_prompts": [
        {
            "title": f"Tell me about {PORTFOLIO_OWNER['name']}'s experience",
            "subtitle": "Work history and roles"
        },
        {
            "title": f"What are {PORTFOLIO_OWNER['name']}'s main skills?",
            "subtitle": "Technical and soft skills"
        },
        {
            "title": f"Show me {PORTFOLIO_OWNER['name']}'s projects",
            "subtitle": "Notable works and contributions"
        },
        {
            "title": f"What is {PORTFOLIO_OWNER['name']}'s education?",
            "subtitle": "Academic background"
        },
    ]
}

# ============ SERVER CONFIG ============
SERVER_CONFIG = {
    "host": os.getenv("SERVER_HOST", "0.0.0.0"),
    "port": int(os.getenv("SERVER_PORT", "8000")),
    "debug": DEBUG,
    "cors_origins": CORS_ORIGINS,
}

# ============ FEATURE FLAGS ============
FEATURES = {
    "enable_chat_history": os.getenv("FEATURE_CHAT_HISTORY", "true").lower() == "true",
    "enable_share_conversations": os.getenv("FEATURE_SHARE_CONVERSATIONS", "true").lower() == "true",
    "enable_cv_download": os.getenv("FEATURE_CV_DOWNLOAD", "true").lower() == "true",
    "enable_contact_form": os.getenv("FEATURE_CONTACT_FORM", "false").lower() == "true",
    "enable_analytics": os.getenv("FEATURE_ANALYTICS", "false").lower() == "true",
}

# ============ LOGGING CONFIG ============
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO" if ENVIRONMENT == "production" else "DEBUG"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# ============ RATE LIMITING ============
API_RATE_LIMIT = {
    "chat": (10, 60),  # 10 requests per 60 seconds for /chat
    "general": (100, 60),  # 100 requests per 60 seconds for other endpoints
    "ingest": (5, 300),  # 5 requests per 5 minutes for /ingest-cv
}


def get_system_prompt():
    """Get the configured system prompt with owner name"""
    return CHAT_CONFIG["system_prompt"].format(name=PORTFOLIO_OWNER["name"])


def validate_config():
    """Validate critical configuration on startup"""
    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY environment variable is required")
    
    if ENVIRONMENT == "production" and DEBUG:
        raise ValueError("DEBUG must be False in production")
    
    if ENVIRONMENT == "production" and SECRET_KEY == "dev-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must be changed in production")
    
    return True
