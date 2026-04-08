# Sujan Maharjan - AI-Powered Portfolio

A modern, ChatGPT-styled portfolio website that uses RAG (Retrieval-Augmented Generation) to allow visitors to learn about you through an intelligent conversational interface.

## Features

✨ **ChatGPT-Styled Interface** - Modern, responsive design with dark grey color scheme  
🤖 **RAG-Powered Chat** - Intelligent responses using your CV as knowledge base  
💾 **Chat History** - Persistent conversation storage with SQLite  
🔗 **Share Conversations** - Generate shareable links for specific chats  
📱 **Responsive Design** - Works seamlessly on mobile and desktop  
📥 **Download CV** - Direct CV download option  
📞 **Contact Integration** - Social links (LinkedIn, GitHub, etc.)  
⚡ **Fast & Efficient** - Python backend with FastAPI + React frontend  

## Tech Stack

### Backend
- **Framework**: FastAPI
- **RAG**: Chroma (Vector Database)
- **Embeddings**: OpenAI Embeddings API
- **Database**: SQLite (Chat History)
- **Language**: Python 3.8+

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS + Custom CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React Icons
- **Date Handling**: date-fns

## Project Structure

```
Portfolio_Ver2/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── rag_system.py          # RAG system with Chroma
│   ├── chat_history.py        # Chat history management
│   ├── ingest_cv.py           # CV ingestion script
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.js     # Sidebar with chat history
│   │   │   ├── ChatWindow.js  # Main chat interface
│   │   │   └── MessageBubble.js # Message display
│   │   ├── api.js             # API client
│   │   ├── App.js             # Main app component
│   │   ├── index.js           # Entry point
│   │   └── index.css          # Tailwind & custom styles
│   ├── public/
│   │   └── index.html         # HTML template
│   ├── package.json           # Node dependencies
│   ├── tailwind.config.js     # Tailwind configuration
│   ├── postcss.config.js      # PostCSS configuration
│   └── .env.example           # Environment variables template
│
└── data/
    └── (Vector DB storage)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- OpenRouter API Key (get one at https://openrouter.io)

### Step 1: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your OpenRouter API key
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
nano .env  # or use your preferred editor
```

### Step 2: Ingest CV Data

```bash
# Run the CV ingestion script to populate the knowledge base
python ingest_cv.py

# You should see:
# ✓ CV data ingested successfully!
# The portfolio knowledge base is now ready to use.
```

### Step 3: Start Backend Server

```bash
# From the backend directory
python main.py

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Step 4: Set Up Frontend

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start

# Frontend will open at http://localhost:3000
```

## API Endpoints

### Chat Operations
- `POST /chat` - Send a message and get a response
- `POST /conversations` - Create a new conversation
- `GET /conversations` - Get all conversations
- `GET /conversations/{id}` - Get conversation history
- `DELETE /conversations/{id}` - Delete a conversation
- `POST /conversations/{id}/share` - Generate share link
- `GET /shared/{share_id}` - Get shared conversation

### Portfolio Operations
- `GET /portfolio-info` - Get portfolio basic info
- `GET /health` - Health check

## Usage

### For Users
1. Visit http://localhost:3000
2. Start a new chat or select from history
3. Ask questions about Sujan's experience, skills, and projects
4. Share interesting conversations using the share button
5. Download the CV using the download button

### For Developers

**Customizing the CV:**
Edit [backend/ingest_cv.py](backend/ingest_cv.py) and update the `CV_DATA` variable with your information, then run:
```bash
python ingest_cv.py
```

**Changing UI Colors:**
Edit [frontend/src/index.css](frontend/src/index.css) and [frontend/tailwind.config.js](frontend/tailwind.config.js) to modify the grey color scheme.

**Adding New Features:**
1. Backend: Add new endpoints in `main.py`
2. Frontend: Add components in `src/components/`
3. API calls: Update `src/api.js`

## Environment Variables

### Backend (.env)
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## Color Scheme

The portfolio uses a professional grey color palette:
- **Dark Grey** (#1a1a1a) - Main background
- **Medium Grey** (#2d2d30) - Secondary background
- **Light Grey** (#3e3e42) - Tertiary elements
- **Lighter Grey** (#ececf1) - Text and primary content
- **Blue** (#3b82f6) - Accent and interactive elements

## Database Schema

### Conversations Table
- `id` (TEXT, PRIMARY KEY) - UUID
- `title` (TEXT) - Chat title
- `created_at` (TEXT) - Creation timestamp
- `updated_at` (TEXT) - Last update timestamp
- `is_shared` (INTEGER) - Share status
- `share_id` (TEXT) - Unique share identifier

### Messages Table
- `id` (TEXT, PRIMARY KEY) - UUID
- `conversation_id` (TEXT) - Foreign key
- `role` (TEXT) - "user" or "assistant"
- `content` (TEXT) - Message content
- `created_at` (TEXT) - Creation timestamp

## Deployment

### Deploy Backend (Example: Render, Railway, Heroku)
1. Push to GitHub
2. Connect repository
3. Set environment variables
4. Deploy

### Deploy Frontend (Example: Vercel, Netlify)
1. Push to GitHub
2. Connect repository
3. Set `REACT_APP_API_URL` to your backend URL
4. Deploy

## Customization Tips

### Update Portfolio Information
Edit the hardcoded info in `backend/main.py` in the `/portfolio-info` endpoint.

### Customize Chat Behavior
Modify the system prompt in `backend/rag_system.py` in the `generate_response` method.

### Add More Projects
Update the CV in `backend/ingest_cv.py` and re-run `python ingest_cv.py`.

### Change Styling
Use Tailwind CSS classes or modify `src/index.css` for custom styles.

## Troubleshooting

**Issue: "OPENROUTER_API_KEY not found"**
- Make sure you have created `.env` file in the backend directory
- Add your OpenRouter API key to the file

**Issue: Frontend can't connect to backend**
- Ensure backend is running on http://localhost:8000
- Check `REACT_APP_API_URL` in frontend `.env`
- Verify CORS is properly configured

**Issue: No responses from AI**
- Check your OpenAI API key validity
- Verify your API account has available credits
- Check console for error messages

**Issue: Database errors**
- Delete `chat_history.db` and `chroma_db` directories to reset
- Re-run `python ingest_cv.py` to reinitialize

## Performance Tips

1. **Embeddings Caching**: Chroma automatically caches embeddings
2. **Connection Pooling**: FastAPI handles this automatically
3. **Frontend Optimization**: React dev tools to check for unnecessary renders
4. **API Response Caching**: Consider adding Redis for production

## Security Considerations

- Never commit `.env` files with real API keys
- Validate all user inputs on the backend
- Implement rate limiting for production
- Use HTTPS in production
- Add authentication if needed

## Future Enhancements

- [ ] Add user authentication
- [ ] Implement PDF resume download
- [ ] Add more AI models support
- [ ] Email notifications for messages
- [ ] Analytics and insights
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Dark/Light mode toggle

## License

This project is open source and available for personal use.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: mhrjnsujan.official@gmail.com
- LinkedIn: https://www.linkedin.com/in/sujan-maharjan-870b46252/

---

**Built with ❤️ by Sujan Maharjan**
