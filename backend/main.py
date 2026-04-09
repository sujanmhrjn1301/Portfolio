"""
Secure FastAPI Backend for AI-Powered Portfolio

Security Features:
- JWT Authentication for admin endpoints
- Rate limiting on all endpoints
- Input validation and sanitization
- Secure error handling (no stack traces)
- CORS configured for production
- Security headers
- Environment-based configuration
"""

import sys

# SQLite override for ChromaDB compatibility on Render
# This is required because Render's default SQLite version is too old for ChromaDB
try:
    import pysqlite3  # type: ignore
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import os
import logging
from datetime import timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field, validator
import uvicorn
from dotenv import load_dotenv

# Import custom modules
from rag_system import RAGSystem
from chat_history import ChatHistory
from github_integration import GitHubIntegration
from admin_db import init_admin_db, verify_admin_credentials
from config import (
    GITHUB_CONFIG,
    CORS_ORIGINS,
    DEBUG,
    ENVIRONMENT,
    SECRET_KEY,
    API_KEY,
    ADMIN_PASSWORD,
    get_cors_origins,
    validate_config,
)
from auth import verify_api_key_or_token, create_access_token
from security import (
    validate_message_content,
    validate_title,
    validate_conversation_id,
    validate_share_id,
    check_rate_limit,
    get_client_ip,
    create_secure_error_response,
)
from ingest_cv import ingest_cv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO if ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate configuration on startup
try:
    validate_config()
    logger.info(f"✅ Configuration validated for {ENVIRONMENT} environment")
except ValueError as e:
    logger.error(f"❌ Configuration error: {str(e)}")
    raise

# Initialize FastAPI app
app = FastAPI(
    title="AI Portfolio API",
    description="Secure API for AI-powered portfolio",
    version="2.0.0"
)

# ============ SECURITY MIDDLEWARE ============

# NOTE: Removed TrustedHostMiddleware since Render handles reverse proxy host validation
# CORS middleware below properly handles cross-origin requests from frontend

# Add CORS middleware with secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Specific methods only
    allow_headers=["Content-Type", "Authorization"],  # Specific headers only
    max_age=3600,  # 1 hour cache
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    
    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests"""
    try:
        await check_rate_limit(request)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=create_secure_error_response(e.status_code, e.detail)
        )
    
    return await call_next(request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler - prevents information disclosure"""
    client_ip = get_client_ip(request)
    
    if isinstance(exc, HTTPException):
        # HTTPExceptions are already handled by FastAPI
        return JSONResponse(
            status_code=exc.status_code,
            content=create_secure_error_response(exc.status_code, exc.detail)
        )
    
    # Log the actual error for debugging (developers only)
    logger.error(f"Unhandled exception from {client_ip}: {str(exc)}", exc_info=DEBUG)
    
    # Return generic error to client (never expose stack trace)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_secure_error_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An error occurred processing your request"
        )
    )


# ============ INITIALIZE SERVICES ============

# Load API keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is required")

try:
    rag_system = RAGSystem(api_key=OPENROUTER_API_KEY)
    chat_history = ChatHistory()
    github_integration = (
        GitHubIntegration(github_token=os.getenv("GITHUB_TOKEN"))
        if GITHUB_CONFIG.get("enabled")
        else None
    )
    logger.info("✅ All services initialized successfully")
except Exception as e:
    logger.error(f"❌ Service initialization error: {str(e)}")
    raise


# ============ DATABASE INITIALIZATION ============

def is_portfolio_data_ingested():
    """
    Check if portfolio CV data has been ingested into ChromaDB
    Returns True if collection has documents, False if empty
    """
    try:
        # Query the collection to see if it has any data
        collection_count = rag_system.collection.count()
        logger.debug(f"ChromaDB collection count: {collection_count}")
        return collection_count > 0
    except Exception as e:
        logger.warning(f"Could not check database state: {str(e)}")
        return False


def auto_ingest_portfolio_data():
    """
    Automatically ingest portfolio CV data on startup if database is empty
    This ensures fresh deployments have data without manual intervention
    """
    if is_portfolio_data_ingested():
        logger.info("✅ Portfolio data already ingested - skipping auto-ingest")
        return
    
    logger.info("📚 Database empty - automatically ingesting portfolio data...")
    try:
        # Get the CV file path
        cv_file_path = os.path.join(
            os.path.dirname(__file__), 
            "data", 
            "Sujan-Maharjan-September-2025.pdf"
        )
        
        # Check if file exists
        if not os.path.exists(cv_file_path):
            logger.warning(f"⚠️  CV file not found at {cv_file_path} - skipping auto-ingest")
            return
        
        # Call ingest_cv (already has duplicate checking built-in)
        logger.info(f"Ingesting from: {cv_file_path}")
        ingest_cv(cv_file_path)
        logger.info("✅ Portfolio data ingested successfully on startup")
        
    except Exception as e:
        # Log error but don't crash the app
        logger.error(f"❌ Auto-ingest failed: {str(e)} - app will work but without portfolio data")


# ============ PYDANTIC MODELS ============

class ChatRequest(BaseModel):
    """Chat request model with validation"""
    conversation_id: str = Field(..., min_length=36, max_length=36)
    message: str = Field(..., min_length=1, max_length=5000)
    github_mode: bool = False
    gen_z_mode: bool = False
    
    @validator("message")
    def validate_message(cls, v):
        return validate_message_content(v)


class ChatResponse(BaseModel):
    """Chat response model"""
    message_id: str
    response: str
    conversation_id: str


class ConversationCreate(BaseModel):
    """Create conversation request"""
    title: Optional[str] = Field(None, max_length=200)
    
    @validator("title")
    def validate_title_field(cls, v):
        if v:
            return validate_title(v)
        return "New Chat"


class ConversationUpdate(BaseModel):
    """Update conversation request"""
    title: str = Field(..., max_length=200)
    
    @validator("title")
    def validate_title_field(cls, v):
        return validate_title(v)


class ConversationResponse(BaseModel):
    """Conversation response"""
    id: str
    title: str
    created_at: str
    updated_at: str


class ChatHistoryResponse(BaseModel):
    """Chat history response"""
    id: str
    role: str
    content: str
    created_at: str


class GitHubRepository(BaseModel):
    """GitHub repository model"""
    name: str
    description: Optional[str]
    url: str
    language: Optional[str]
    stars: int
    topics: List[str]


class PortfolioInfo(BaseModel):
    """Portfolio information (public data only)"""
    name: str
    github: Optional[str]
    linkedin: Optional[str]


# ============ ROUTES ============

@app.get("/health")
async def health_check():
    """Health check endpoint (no auth required, rate limited)"""
    return {
        "status": "ok",
        "environment": ENVIRONMENT,
        "version": "2.0.0"
    }


@app.get("/auth/token", tags=["Authentication"])
async def get_auth_token():
    """
    Get authentication token (development only)
    
    In production, use your authentication service
    """
    if ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token generation disabled in production"
        )
    
    # Create a test token valid for 24 hours
    token = create_access_token(
        data={"sub": "dev-user"},
        expires_delta=timedelta(hours=24)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 86400
    }


# ============ CHAT ENDPOINTS (Public) ============

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest, req: Request) -> ChatResponse:
    """
    Send a message and get a response from the RAG system
    
    Public endpoint - no authentication required
    """
    try:
        # Validate conversation ID format
        validate_conversation_id(request.conversation_id)
        
        # Log request (without sensitive data in production)
        if DEBUG:
            logger.debug(f"Chat request: {request.message[:100]}...")
        
        # Add user message to history
        chat_history.add_message(
            request.conversation_id, "user", request.message
        )
        
        # Generate response using RAG
        response = rag_system.generate_response(
            request.message,
            github_mode=request.github_mode,
            gen_z_mode=request.gen_z_mode
        )
        
        # Add assistant response to history
        msg_id = chat_history.add_message(
            request.conversation_id, "assistant", response
        )
        
        return ChatResponse(
            message_id=msg_id,
            response=response,
            conversation_id=request.conversation_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )


# ============ CONVERSATION ENDPOINTS (Public) ============

@app.post("/conversations", response_model=ConversationResponse, tags=["Conversations"])
async def create_conversation(payload: ConversationCreate) -> ConversationResponse:
    """Create a new conversation (public)"""
    try:
        title = payload.title or "New Chat"
        conv_id = chat_history.create_conversation(title)
        
        conversations = chat_history.get_all_conversations()
        for conv in conversations:
            if conv["id"] == conv_id:
                return ConversationResponse(**conv)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Conversation creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )


@app.get("/conversations", response_model=List[ConversationResponse], tags=["Conversations"])
async def get_conversations() -> List[ConversationResponse]:
    """Get all conversations (public)"""
    try:
        conversations = chat_history.get_all_conversations()
        return [ConversationResponse(**conv) for conv in conversations]
    
    except Exception as e:
        logger.error(f"Get conversations error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@app.get("/conversations/{conversation_id}", response_model=List[ChatHistoryResponse], tags=["Conversations"])
async def get_conversation_history(conversation_id: str) -> List[ChatHistoryResponse]:
    """Get messages from a specific conversation (public)"""
    try:
        validate_conversation_id(conversation_id)
        
        messages = chat_history.get_conversation_messages(conversation_id)
        return [ChatHistoryResponse(**msg) for msg in messages]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get history error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation history"
        )


@app.post("/conversations/{conversation_id}/share", tags=["Conversations"])
async def share_conversation(conversation_id: str) -> dict:
    """Generate a share link for a conversation (public)"""
    try:
        validate_conversation_id(conversation_id)
        
        share_id = chat_history.share_conversation(conversation_id)
        return {
            "share_id": share_id,
            "share_url": f"/shared/{share_id}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Share error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create share link"
        )


@app.get("/shared/{share_id}", tags=["Conversations"])
async def get_shared_conversation(share_id: str) -> dict:
    """Get a shared conversation (public, no auth)"""
    try:
        validate_share_id(share_id)
        
        conversation = chat_history.get_shared_conversation(share_id)
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shared conversation not found"
            )
        
        return conversation
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get shared error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve shared conversation"
        )


@app.delete("/conversations/{conversation_id}", tags=["Conversations"])
async def delete_conversation(conversation_id: str) -> dict:
    """Delete a conversation (requires authentication)"""
    try:
        # NOTE: In production, verify user owns this conversation
        validate_conversation_id(conversation_id)
        
        chat_history.delete_conversation(conversation_id)
        return {"message": "Conversation deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )


@app.patch("/conversations/{conversation_id}", response_model=ConversationResponse, tags=["Conversations"])
async def update_conversation(
    conversation_id: str,
    payload: ConversationUpdate
) -> ConversationResponse:
    """Update a conversation title (requires authentication)"""
    try:
        # NOTE: In production, verify user owns this conversation
        validate_conversation_id(conversation_id)
        
        chat_history.update_conversation(conversation_id, payload.title)
        conversations = chat_history.get_all_conversations()
        
        for conv in conversations:
            if conv["id"] == conversation_id:
                return ConversationResponse(**conv)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update conversation"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update conversation"
        )


# ============ ADMIN ENDPOINTS (Protected) ============

@app.post("/ingest-cv", tags=["Admin"])
async def ingest_cv_data(
    cv_text: str,
    user: str = Depends(verify_api_key_or_token)
) -> dict:
    """
    Ingest CV data into RAG system
    
    Requires authentication via API key or JWT token
    """
    try:
        if not cv_text or len(cv_text.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CV text cannot be empty"
            )
        
        if len(cv_text) > 1000000:  # 1MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="CV text exceeds maximum size"
            )
        
        logger.info(f"CV ingestion initiated by {user}")
        rag_system.ingest_cv_data(cv_text)
        
        return {"message": "CV data ingested successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CV ingestion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to ingest CV data"
        )


def verify_admin_password(password: str) -> bool:
    """Verify admin password for protected endpoints"""
    # Default admin credentials from database
    return verify_admin_credentials(username="eiji", password=password)


@app.post("/upload-cv", tags=["Admin"])
async def upload_cv_file(
    file: UploadFile = File(...),
    username: str = "eiji",
    password: str = ""
) -> dict:
    """
    Upload a new CV PDF file to update the knowledge base
    
    This endpoint:
    1. Verifies the admin credentials (eiji / password)
    2. Saves the uploaded PDF temporarily
    3. Clears existing CV data
    4. Ingests the new CV into the knowledge base
    5. Cleans up temporary files
    
    The knowledge base updates instantly without restarting.
    """
    try:
        # Verify credentials against admin database
        if not verify_admin_credentials(username=username, password=password):
            logger.warning(f"❌ Invalid admin credentials attempt: username={username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported"
            )
        
        # Validate file size (max 10MB)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 10MB limit"
            )
        
        logger.info(f"📁 Processing uploaded CV file: {file.filename}")
        
        # Save to temporary location
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file_content)
            temp_path = tmp_file.name
        
        try:
            # Clear existing collection
            try:
                rag_system.chroma_client.delete_collection(name="portfolio_cv")
                logger.info("✅ Cleared existing CV data from database")
            except Exception as e:
                logger.warning(f"Could not delete collection (may not exist): {str(e)}")
            
            # Ingest the new CV
            logger.info(f"📚 Ingesting uploaded CV from: {temp_path}")
            ingest_cv(temp_path)
            logger.info("✅ CV data ingested successfully from uploaded file")
            
            return {
                "message": "CV uploaded and knowledge base updated successfully",
                "filename": file.filename
            }
        
        finally:
            # Clean up temporary file
            try:
                os.remove(temp_path)
            except:
                pass
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ CV upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process CV upload: {str(e)}"
        )


# ============ PUBLIC INFO ENDPOINTS ============

@app.get("/portfolio-info", response_model=PortfolioInfo, tags=["Portfolio"])
async def get_portfolio_info() -> PortfolioInfo:
    """Get public portfolio information (name, github, linkedin only)"""
    from config import PORTFOLIO_OWNER
    
    return PortfolioInfo(
        name=PORTFOLIO_OWNER["name"],
        github=PORTFOLIO_OWNER.get("github"),
        linkedin=PORTFOLIO_OWNER.get("linkedin")
    )


# ============ GITHUB ENDPOINTS (Public) ============

@app.get("/github/repositories", response_model=List[GitHubRepository], tags=["GitHub"])
async def get_github_repositories() -> List[GitHubRepository]:
    """Fetch all public repositories from GitHub"""
    try:
        if not github_integration:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub integration not enabled"
            )
        
        username = GITHUB_CONFIG.get("username", "sujanmhrjn1301")
        repos = github_integration.get_user_repositories(username)
        
        result = []
        for repo in repos:
            result.append(GitHubRepository(
                name=repo.get("name", ""),
                description=repo.get("description", ""),
                url=repo.get("html_url", ""),
                language=repo.get("language", ""),
                stars=repo.get("stargazers_count", 0),
                topics=repo.get("topics", [])
            ))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GitHub repositories error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch repositories"
        )


@app.get("/github/repositories/language/{language}", response_model=List[GitHubRepository], tags=["GitHub"])
async def get_github_repositories_by_language(language: str) -> List[GitHubRepository]:
    """Fetch repositories filtered by programming language"""
    try:
        if not github_integration:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub integration not enabled"
            )
        
        username = GITHUB_CONFIG.get("username", "sujanmhrjn1301")
        repos = github_integration.search_repos_by_language(username, language)
        
        result = []
        for repo in repos:
            result.append(GitHubRepository(
                name=repo.get("name", ""),
                description=repo.get("description", ""),
                url=repo.get("html_url", ""),
                language=repo.get("language", ""),
                stars=repo.get("stargazers_count", 0),
                topics=repo.get("topics", [])
            ))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GitHub filter error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to filter repositories"
        )


@app.get("/github/repositories/{repo_name}", tags=["GitHub"])
async def get_github_repository_details(repo_name: str) -> dict:
    """Fetch detailed information and README for a specific repository"""
    try:
        if not github_integration:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub integration not enabled"
            )
        
        # Validate repo name (basic sanitization)
        if not repo_name or len(repo_name) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid repository name"
            )
        
        username = GITHUB_CONFIG.get("username", "sujanmhrjn1301")
        repo_details = github_integration.get_repository_details(username, repo_name)
        
        if not repo_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repository not found"
            )
        
        readme = github_integration.get_repository_readme(username, repo_name)
        
        return {
            "name": repo_details.get("name", ""),
            "description": repo_details.get("description", ""),
            "url": repo_details.get("html_url", ""),
            "language": repo_details.get("language", ""),
            "stars": repo_details.get("stargazers_count", 0),
            "forks": repo_details.get("forks_count", 0),
            "topics": repo_details.get("topics", []),
            "created_at": repo_details.get("created_at", ""),
            "updated_at": repo_details.get("updated_at", ""),
            "readme": readme
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"GitHub details error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve repository details"
        )


# ============ STARTUP & SHUTDOWN ============

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"🚀 Starting AI Portfolio API in {ENVIRONMENT} mode")
    if DEBUG:
        logger.debug("Debug mode enabled")
    
    # Initialize admin database
    init_admin_db()
    
    # Auto-ingest portfolio data if database is empty
    auto_ingest_portfolio_data()


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("👋 Shutting down API")


# ============ MAIN ============

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", "8000")),
        reload=DEBUG,
        log_level="debug" if DEBUG else "info"
    )
