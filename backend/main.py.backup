from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from rag_system import RAGSystem
from chat_history import ChatHistory
from github_integration import GitHubIntegration
from config import GITHUB_CONFIG
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Sujan's Portfolio API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system and chat history
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

rag_system = RAGSystem(api_key=OPENROUTER_API_KEY)
chat_history = ChatHistory()

# Initialize GitHub integration
github_token = os.getenv("GITHUB_TOKEN")
github_integration = GitHubIntegration(github_token=github_token) if GITHUB_CONFIG.get("enabled") else None

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    github_mode: bool = False
    gen_z_mode: bool = False

class ChatResponse(BaseModel):
    message_id: str
    response: str
    conversation_id: str

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Chat"

class ConversationUpdate(BaseModel):
    title: str

class GitHubRepository(BaseModel):
    name: str
    description: Optional[str]
    url: str
    language: Optional[str]
    stars: int
    topics: List[str]

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: str

class ChatHistoryResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: str

# Routes

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    """Send a message and get a response from the RAG system"""
    try:
        print(f"\n🔵 Chat Request: {request.message} (GitHub Mode: {request.github_mode}, Gen-Z Mode: {request.gen_z_mode})")
        # Add user message to history
        chat_history.add_message(request.conversation_id, "user", request.message)
        
        # Generate response using RAG with optional modes
        response = rag_system.generate_response(request.message, github_mode=request.github_mode, gen_z_mode=request.gen_z_mode)
        
        # Add assistant response to history
        msg_id = chat_history.add_message(request.conversation_id, "assistant", response)
        
        print(f"✅ Chat Response: {response[:100]}...")
        return ChatResponse(
            message_id=msg_id,
            response=response,
            conversation_id=request.conversation_id
        )
    
    except Exception as e:
        print(f"❌ Chat Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/conversations")
def create_conversation(payload: ConversationCreate) -> ConversationResponse:
    """Create a new conversation"""
    try:
        # Use default "New Chat" if title is None
        title = payload.title if payload.title else "New Chat"
        conv_id = chat_history.create_conversation(title)
        conversations = chat_history.get_all_conversations()
        
        for conv in conversations:
            if conv['id'] == conv_id:
                return ConversationResponse(**conv)
        
        # If conversation not found, raise error
        raise HTTPException(status_code=500, detail="Failed to create conversation")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations")
def get_conversations() -> List[ConversationResponse]:
    """Get all conversations"""
    try:
        conversations = chat_history.get_all_conversations()
        return [ConversationResponse(**conv) for conv in conversations]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}")
def get_conversation_history(conversation_id: str) -> List[ChatHistoryResponse]:
    """Get messages from a specific conversation"""
    try:
        messages = chat_history.get_conversation_messages(conversation_id)
        return [ChatHistoryResponse(**msg) for msg in messages]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/conversations/{conversation_id}/share")
def share_conversation(conversation_id: str) -> dict:
    """Generate a share link for a conversation"""
    try:
        share_id = chat_history.share_conversation(conversation_id)
        return {"share_id": share_id, "share_url": f"/shared/{share_id}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/shared/{share_id}")
def get_shared_conversation(share_id: str) -> dict:
    """Get a shared conversation"""
    try:
        conversation = chat_history.get_shared_conversation(share_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Shared conversation not found")
        
        return conversation
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str) -> dict:
    """Delete a conversation"""
    try:
        chat_history.delete_conversation(conversation_id)
        return {"message": "Conversation deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/conversations/{conversation_id}")
def update_conversation(conversation_id: str, payload: ConversationUpdate) -> ConversationResponse:
    """Update a conversation title"""
    try:
        chat_history.update_conversation(conversation_id, payload.title)
        conversations = chat_history.get_all_conversations()
        
        for conv in conversations:
            if conv['id'] == conversation_id:
                return ConversationResponse(**conv)
        
        raise HTTPException(status_code=500, detail="Failed to update conversation")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-cv")
def ingest_cv_data(cv_text: str):
    """Ingest CV data into the RAG system (for initialization)"""
    try:
        rag_system.ingest_cv_data(cv_text)
        return {"message": "CV data ingested successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio-info")
def get_portfolio_info() -> dict:
    """Get basic portfolio information"""
    return {
        "name": "Sujan Maharjan",
        "email": "mhrjnsujan.official@gmail.com",
        "phone": "+977-9860942721",
        "github": "https://github.com/sujanmhrjn1301",
        "linkedin": "https://www.linkedin.com/in/sujan-maharjan-870b46252/",
        "location": "Thecho, Lalitpur"
    }

# GitHub Integration Endpoints

@app.get("/github/repositories")
def get_github_repositories() -> List[GitHubRepository]:
    """Fetch all public repositories from GitHub"""
    try:
        if not github_integration:
            raise HTTPException(status_code=503, detail="GitHub integration not enabled")
        
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
    
    except Exception as e:
        print(f"❌ Error fetching GitHub repositories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/github/repositories/language/{language}")
def get_github_repositories_by_language(language: str) -> List[GitHubRepository]:
    """Fetch repositories filtered by programming language"""
    try:
        if not github_integration:
            raise HTTPException(status_code=503, detail="GitHub integration not enabled")
        
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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/github/repositories/{repo_name}")
def get_github_repository_details(repo_name: str) -> dict:
    """Fetch detailed information and README for a specific repository"""
    try:
        if not github_integration:
            raise HTTPException(status_code=503, detail="GitHub integration not enabled")
        
        username = GITHUB_CONFIG.get("username", "sujanmhrjn1301")
        repo_details = github_integration.get_repository_details(username, repo_name)
        readme = github_integration.get_repository_readme(username, repo_name)
        
        if not repo_details:
            raise HTTPException(status_code=404, detail="Repository not found")
        
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
