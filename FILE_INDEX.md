# 📋 Complete File Index & Reference

## Frontend Files

### Configuration Files
| File | Purpose |
|------|---------|
| `package.json` | Node dependencies & scripts |
| `tailwind.config.js` | Tailwind CSS configuration |
| `postcss.config.js` | PostCSS configuration |
| `.env.example` | Environment variables template |
| `Dockerfile` | Docker containerization |

### Source Files
| File | Purpose |
|------|---------|
| `src/index.js` | React entry point |
| `src/App.js` | Main app component with routing |
| `src/api.js` | REST API client |
| `src/index.css` | Tailwind imports + custom styles |
| `src/components/Sidebar.js` | Navigation & chat history |
| `src/components/ChatWindow.js` | Main chat interface |
| `src/components/MessageBubble.js` | Message display component |
| `src/components/SharedView.js` | Shared conversation viewer |

### Public Files
| File | Purpose |
|------|---------|
| `public/index.html` | HTML template |

---

## Backend Files

### Application Files
| File | Purpose |
|------|---------|
| `main.py` | FastAPI application & routes |
| `rag_system.py` | RAG engine with Chroma |
| `chat_history.py` | Chat history management |
| `config.py` | Configuration management |
| `ingest_cv.py` | CV data ingestion script |
| `cli.py` | Command-line management tool |

### Configuration Files
| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment template |
| `Dockerfile` | Docker containerization |

---

## Root Level Files

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Complete documentation |
| `QUICKSTART.md` | 5-minute setup guide |
| `ARCHITECTURE.md` | System design & flows |
| `PROJECT_SUMMARY.md` | Project overview (this guide) |
| `FILE_INDEX.md` | This file |

### Configuration
| File | Purpose |
|------|---------|
| `docker-compose.yml` | Docker Compose orchestration |
| `.gitignore` | Git ignore patterns |

---

## Complete Directory Tree

```
Portfolio_Ver2/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick setup guide
├── 📄 ARCHITECTURE.md              # System architecture
├── 📄 PROJECT_SUMMARY.md           # Project overview
├── 📄 FILE_INDEX.md                # This file
├── 📄 docker-compose.yml           # Docker composition
├── 📄 .gitignore                   # Git ignore
│
├── 📁 backend/
│   ├── main.py                     # FastAPI app
│   ├── rag_system.py               # RAG system
│   ├── chat_history.py             # History management
│   ├── config.py                   # Configuration
│   ├── ingest_cv.py                # CV ingestion
│   ├── cli.py                      # CLI tool
│   ├── requirements.txt            # Dependencies
│   ├── .env.example                # Env template
│   ├── Dockerfile                  # Docker build
│   │
│   └── 📁 (Generated at runtime)
│       ├── venv/                   # Virtual environment
│       ├── chroma_db/              # Vector database
│       ├── chat_history.db         # SQLite database
│       └── __pycache__/            # Python cache
│
├── 📁 frontend/
│   ├── package.json                # Node config
│   ├── tailwind.config.js          # Tailwind config
│   ├── postcss.config.js           # PostCSS config
│   ├── .env.example                # Env template
│   ├── Dockerfile                  # Docker build
│   │
│   ├── 📁 src/
│   │   ├── index.js                # Entry point
│   │   ├── App.js                  # Main component
│   │   ├── api.js                  # API client
│   │   ├── index.css               # Styles
│   │   │
│   │   └── 📁 components/
│   │       ├── Sidebar.js          # Sidebar component
│   │       ├── ChatWindow.js       # Chat interface
│   │       ├── MessageBubble.js    # Message display
│   │       └── SharedView.js       # Share viewer
│   │
│   ├── 📁 public/
│   │   └── index.html              # HTML template
│   │
│   └── 📁 (Generated at runtime)
│       ├── node_modules/           # Dependencies
│       └── build/                  # Production build
│
└── 📁 data/
    └── (For future data storage)
```

---

## File Purposes Quick Reference

### Entry Points
- `frontend/public/index.html` - Web entry point
- `frontend/src/index.js` - React initialization
- `backend/main.py` - API server initialization
- `backend/ingest_cv.py` - Data initialization
- `backend/cli.py` - CLI tool entry
- `docker-compose.yml` - Container orchestration

### Core Logic
- `backend/rag_system.py` - AI intelligence
- `backend/chat_history.py` - Data persistence
- `frontend/src/api.js` - API communication
- `frontend/src/App.js` - UI coordination

### Components (Frontend)
- `Sidebar.js` - Navigation interface
- `ChatWindow.js` - Main chat UI
- `MessageBubble.js` - Message rendering
- `SharedView.js` - Share functionality

### Configuration
- `backend/config.py` - Backend settings
- `frontend/tailwind.config.js` - UI styling
- `backend/requirements.txt` - Python packages
- `frontend/package.json` - Node packages
- `.env.example` files - Environment templates

### Documentation
- `README.md` - How to use & deploy
- `QUICKSTART.md` - Setup instructions
- `ARCHITECTURE.md` - System design
- `PROJECT_SUMMARY.md` - Overview
- `FILE_INDEX.md` - This file

---

## Installation Checklist

### Before Starting
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] OpenAI API key obtained
- [ ] Git installed (optional, for versioning)

### Backend Setup
- [ ] Navigate to `backend/` directory
- [ ] Create virtual environment
- [ ] Run `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Add `OPENAI_API_KEY` to `.env`
- [ ] Run `python ingest_cv.py`
- [ ] Run `python main.py`

### Frontend Setup
- [ ] Navigate to `frontend/` directory
- [ ] Run `npm install`
- [ ] Copy `.env.example` to `.env`
- [ ] Run `npm start`

### Verification
- [ ] Backend running at http://localhost:8000
- [ ] API docs at http://localhost:8000/docs
- [ ] Frontend running at http://localhost:3000
- [ ] Chat works and displays messages
- [ ] Sidebar shows portfolio info
- [ ] Share button generates links

---

## Common Tasks & Files to Edit

### Change Portfolio Info
**File**: `backend/config.py`
```python
PORTFOLIO_OWNER = {
    "name": "Your Name",
    "email": "email@example.com",
    # ...
}
```

### Update CV
**File**: `backend/ingest_cv.py`
```python
CV_DATA = """
Your CV content here...
"""
```
Then run: `python ingest_cv.py`

### Customize Colors
**Files**: 
- `frontend/src/index.css` - CSS overrides
- `frontend/tailwind.config.js` - Color definitions

### Change AI Behavior
**File**: `backend/rag_system.py` - `system_prompt` variable

### Add New Endpoints
**File**: `backend/main.py` - Add route functions

### Modify UI Layout
**File**: `frontend/src/App.js` - Component arrangement

### Update API URL
**File**: `frontend/src/api.js` - `API_BASE_URL` variable

---

## Development Workflow

### Start Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate (Windows)
python main.py

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: CLI (optional)
cd backend
python cli.py list
```

### Make Changes
1. Edit component file
2. Save (auto-reload in development)
3. Test in browser
4. Verify in console

### Debug API
- Frontend API errors: Browser DevTools → Network tab
- Backend errors: Terminal output
- Database issues: Use `backend/cli.py` commands

### Build for Production
```bash
# Backend - Docker
docker build -t portfolio-backend ./backend

# Frontend - Production build
cd frontend
npm run build
```

---

## File Dependencies

### Frontend Dependencies
```
App.js
├── requires: Sidebar.js, ChatWindow.js, SharedView.js
├── uses: api.js
│   └── requires: axios
└── styles: index.css (Tailwind + Custom)

Sidebar.js
├── uses: lucide-react (icons)
└── uses: date-fns (date formatting)

ChatWindow.js
├── uses: MessageBubble.js
├── uses: lucide-react
└── uses: api.js

SharedView.js
├── uses: MessageBubble.js
├── uses: react-router-dom
└── uses: api.js
```

### Backend Dependencies
```
main.py
├── imports: FastAPI, SQLAlchemy patterns
├── uses: rag_system.py
├── uses: chat_history.py
├── uses: config.py (settings)
└── requires: openai, chromadb, fastapi

rag_system.py
├── uses: chromadb (Chroma)
├── uses: openai API
└── requires: openai package

chat_history.py
├── uses: sqlite3 (Python standard)
└── requires: no external packages

ingest_cv.py
├── uses: rag_system.py
├── uses: config.py
└── requires: config.py data

cli.py
├── uses: rag_system.py
├── uses: chat_history.py
├── uses: argparse (Python standard)
└── requires: dotenv
```

---

## Size Reference

### Code Files
- `main.py`: ~240 lines
- `rag_system.py`: ~140 lines
- `chat_history.py`: ~180 lines
- `config.py`: ~80 lines
- `cli.py`: ~280 lines
- **Backend Total**: ~900 lines

- `App.js`: ~180 lines
- `Sidebar.js`: ~220 lines
- `ChatWindow.js`: ~200 lines
- `MessageBubble.js`: ~60 lines
- `SharedView.js`: ~110 lines
- `api.js`: ~70 lines
- **Frontend Total**: ~840 lines

**Total Project**: ~1,740 lines of code

---

## Customization Priority

### Must Customize
1. `backend/config.py` - Your information
2. `backend/ingest_cv.py` - Your CV
3. `.env` files - Your API keys

### Should Customize
4. `frontend/tailwind.config.js` - Your brand colors
5. `frontend/src/index.css` - Your styling
6. `backend/config.py` - Quick prompts

### Can Customize Later
7. All other files - Advanced customization

---

## Backup Strategy

### Important Files to Backup
- `backend/.env` - API keys
- `backend/chat_history.db` - Conversation history
- `backend/chroma_db/` - Knowledge base
- `backend/config.py` - Your customizations
- `backend/ingest_cv.py` - Your CV data
- `frontend/.env` - Frontend config

### Backup Commands
```bash
# Backup everything
cp -r backend/chat_history.db backup/
cp -r backend/chroma_db/ backup/
cp backend/config.py backup/
```

---

## Next Steps

1. **Setup**: Follow [QUICKSTART.md](QUICKSTART.md)
2. **Learn**: Read [README.md](README.md) & [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Customize**: Edit `config.py` and `ingest_cv.py`
4. **Test**: Run locally and verify all features
5. **Deploy**: Choose hosting and deploy both services
6. **Share**: Tell people about your portfolio!

---

**For questions, refer to the documentation or check the specific component file.**
