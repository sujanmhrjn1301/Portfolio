# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                             │
│                   (React Frontend)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  REST API Endpoints                                  │  │
│  │  - Chat Operations                                   │  │
│  │  - Conversation Management                           │  │
│  │  - Portfolio Information                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                     │
│        ┌──────────────┼──────────────┐                      │
│        ▼              ▼              ▼                      │
│  ┌─────────┐  ┌──────────┐  ┌─────────────┐               │
│  │   RAG   │  │  OpenAI  │  │   SQLite    │               │
│  │ System  │  │   API    │  │  Database   │               │
│  │ (Chroma)│  │ (GPT)    │  │  (History)  │               │
│  └─────────┘  └──────────┘  └─────────────┘               │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Knowledge Base      │
            │  (CV Embeddings)     │
            │  (Chroma DB)         │
            └──────────────────────┘
```

## Data Flow

### 1. Chat Flow
```
User Input
    │
    ▼
React Component (ChatWindow)
    │
    ▼
API Call (axios) → /chat endpoint
    │
    ▼
FastAPI Backend
    │
    ├─ Save user message to SQLite
    │
    ├─ Retrieve relevant CV chunks from Chroma
    │
    ├─ Send to OpenAI with context
    │
    └─ Get response
    │
    ▼
Save assistant message to SQLite
    │
    ▼
Return response to frontend
    │
    ▼
Display in UI
```

### 2. Initialization Flow
```
Run ingest_cv.py
    │
    ├─ Read CV text
    │
    ├─ Split into chunks (500 chars, 50 char overlap)
    │
    ├─ Generate embeddings via OpenAI API
    │
    ├─ Store in Chroma vector database
    │
    └─ Ready for RAG queries
```

### 3. Conversation Sharing Flow
```
User clicks Share
    │
    ▼
Generate unique share_id
    │
    ▼
Mark as shared in SQLite
    │
    ▼
Create share URL: /shared/{share_id}
    │
    ▼
Copy to clipboard
    │
    ▼
Anyone with URL can view
```

## Component Hierarchy (Frontend)

```
App.js (Root)
├── Router (React Router)
│   ├── Route: / (Main App)
│   │   ├── Sidebar.js
│   │   │   ├── New Chat Button
│   │   │   ├── Chat History List
│   │   │   └── Portfolio Info Card
│   │   │
│   │   └── ChatWindow.js
│   │       ├── Welcome Screen / Message List
│   │       ├── MessageBubble.js (repeated)
│   │       │   ├── User Message
│   │       │   └── Assistant Message
│   │       │
│   │       └── Input Form
│   │
│   └── Route: /shared/:shareId (Shared View)
│       └── SharedView.js
│           ├── Header with back button
│           ├── Message List
│           └── Footer
```

## Database Schema

### SQLite (Chat History)

**Conversations Table**
```sql
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,              -- UUID
  title TEXT,                       -- Chat title
  created_at TEXT,                 -- ISO timestamp
  updated_at TEXT,                 -- ISO timestamp
  is_shared INTEGER DEFAULT 0,     -- Boolean flag
  share_id TEXT UNIQUE              -- Short ID for sharing
)
```

**Messages Table**
```sql
CREATE TABLE messages (
  id TEXT PRIMARY KEY,              -- UUID
  conversation_id TEXT,            -- Foreign key
  role TEXT,                       -- 'user' or 'assistant'
  content TEXT,                    -- Message text
  created_at TEXT,                 -- ISO timestamp
  FOREIGN KEY(conversation_id) REFERENCES conversations(id)
)
```

### Chroma (Vector DB)

**Collection: portfolio_cv**
```
Document Chunks
├── id: cv_chunk_0
├── embedding: [0.123, -0.456, ...] (1536 dimensions)
├── document: "Full text chunk"
└── metadata: {source: "cv", chunk: 0}
```

## API Endpoints

### Base URL: `http://localhost:8000`

#### Chat Operations
- `POST /chat` - Send message
  ```json
  {
    "conversation_id": "uuid",
    "message": "Tell me about experience"
  }
  ```

#### Conversation Management
- `POST /conversations` - Create new conversation
- `GET /conversations` - List all conversations
- `GET /conversations/{id}` - Get conversation history
- `DELETE /conversations/{id}` - Delete conversation
- `POST /conversations/{id}/share` - Generate share link
- `GET /shared/{share_id}` - Get shared conversation

#### Information
- `GET /portfolio-info` - Get portfolio info
- `GET /health` - Health check

## Technology Choices

### Why These Technologies?

**FastAPI**
- ✅ Modern, fast, built-in validation
- ✅ Automatic API documentation
- ✅ Easy to deploy
- ✅ Great async support

**React**
- ✅ Popular, large ecosystem
- ✅ Excellent for interactive UIs
- ✅ Component reusability
- ✅ Good performance

**Chroma**
- ✅ Simple vector DB setup
- ✅ No external dependencies
- ✅ Built-in embedding support
- ✅ SQLite-based persistence

**OpenAI API**
- ✅ State-of-the-art models
- ✅ Reliable service
- ✅ Well-documented
- ✅ Good for Q&A tasks

**SQLite**
- ✅ Zero configuration
- ✅ No server needed
- ✅ Great for small to medium data
- ✅ Easy to backup

**Tailwind CSS**
- ✅ Rapid UI development
- ✅ Consistent styling
- ✅ Great grey palette support
- ✅ Mobile-first design

## Performance Considerations

### Frontend
- Lazy loading of conversation history
- Efficient re-rendering with React
- Message virtualization for large histories
- Debounced input

### Backend
- Connection pooling for database
- Embedding caching in Chroma
- Async operations with FastAPI
- Chunking strategy for large CVs

### Databases
- Indexed queries on SQLite
- Cosine similarity search in Chroma
- Batch operations support

## Security Considerations

### Current Implementation
- API keys in environment variables
- CORS restrictions to localhost
- No authentication (local use)

### Production Recommendations
- Use HTTPS/TLS
- Implement authentication (JWT, OAuth)
- Rate limiting on API endpoints
- Input validation and sanitization
- API key rotation strategy
- SQL injection prevention (using parameterized queries)
- XSS prevention (React built-in)

## Scaling Opportunities

1. **Database** → PostgreSQL with pgvector
2. **Vector DB** → Pinecone, Weaviate
3. **Caching** → Redis for embeddings
4. **Async** → Celery for background jobs
5. **Frontend** → Next.js for better performance
6. **Authentication** → Auth0, Firebase
7. **Monitoring** → Sentry, DataDog
8. **Analytics** → Mixpanel, Amplitude

## Deployment Considerations

### Docker
- Multi-stage builds for frontend
- Lightweight Python image for backend
- Volume mounts for data persistence

### Cloud Platforms
- **Vercel** - Frontend deployment
- **Railway/Render** - Backend deployment
- **AWS RDS** - Production database
- **Pinecone/Weaviate** - Managed vector DB

### CI/CD
- GitHub Actions for testing
- Automated deployments on push
- Environment-based configuration

## Testing Strategy

### Frontend
- Unit tests with Jest
- Component tests with React Testing Library
- E2E tests with Cypress

### Backend
- Unit tests with pytest
- Integration tests for API endpoints
- Load testing with Locust

### CI/CD
- Automated tests on every commit
- Pre-deployment testing
- Staging environment validation
