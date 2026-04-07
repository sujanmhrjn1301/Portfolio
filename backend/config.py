"""
Portfolio Configuration
Customize your portfolio settings here
"""

# Portfolio Owner Information
PORTFOLIO_OWNER = {
    "name": "Sujan Maharjan",
    "email": "mhrjnsujan.official@gmail.com",
    "phone": "+977-9860942721",
    "location": "Thecho, Lalitpur",
    "github": "https://github.com/sujanmhrjn1301",
    "linkedin": "https://www.linkedin.com/in/sujan-maharjan-870b46252/",
}

# Chat Settings
CHAT_CONFIG = {
    "model": "openai/gpt-4o-mini",
    "temperature": 0.4,
    "max_tokens": 350,
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

# RAG Settings
RAG_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "distance_threshold": 1.5,
    "n_results": 5,
    "embedding_model": "text-embedding-3-small",
    "collection_name": "portfolio_cv",
}

# Database Settings
DATABASE_CONFIG = {
    "chat_history_db": "./chat_history.db",
    "chroma_db_path": "./chroma_db",
}

# GitHub Integration Settings
GITHUB_CONFIG = {
    "enabled": True,
    "username": "sujanmhrjn1301",
    "token": None,  # Will be loaded from environment variable GITHUB_TOKEN
    "include_readme": True,
    "include_stars": True,
    "include_languages": True,
    "include_topics": True,
}

# UI Configuration
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

# Server Settings
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False,
    "cors_origins": [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
}

# Feature Flags
FEATURES = {
    "enable_chat_history": True,
    "enable_share_conversations": True,
    "enable_cv_download": True,
    "enable_contact_form": True,
    "enable_analytics": False,
}


def get_system_prompt():
    """Get the configured system prompt with owner name"""
    return CHAT_CONFIG["system_prompt"].format(name=PORTFOLIO_OWNER["name"])
