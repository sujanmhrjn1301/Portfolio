# Quick Start Guide

Get your AI-powered portfolio running in 5 minutes! 🚀

## Prerequisites
- Python 3.8+
- Node.js 16+
- OpenRouter API Key (get one at https://openrouter.io)

## Windows Users

### Step 1: Set Up Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Open `backend/.env.example`
2. Copy it as `backend/.env`
3. Add your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-...your-key-here...
```

### Step 3: Ingest Your CV
```bash
python ingest_cv.py
```
You should see: `✓ CV data ingested successfully!`

### Step 4: Start Backend
```bash
python main.py
```
Backend runs at: http://localhost:8000

### Step 5: Set Up Frontend (New Terminal)
```bash
cd frontend
npm install
npm start
```
Frontend opens at: http://localhost:3000

---

## Mac/Linux Users

### Step 1: Set Up Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
cp .env.example .env
nano .env  # Add your OpenRouter API key
```

### Step 3: Ingest Your CV
```bash
python3 ingest_cv.py
```

### Step 4: Start Backend
```bash
python3 main.py
```

### Step 5: Set Up Frontend (New Terminal)
```bash
cd frontend
npm install
npm start
```

---

## What to Do Next

### ✏️ Customize Your Portfolio
1. Edit `backend/ingest_cv.py` - Update the `CV_DATA` variable with your info
2. Run `python ingest_cv.py` again to reload
3. Edit `backend/main.py` - Update `/portfolio-info` with your social links
4. Refresh browser to see changes

### 🎨 Change Colors
Edit `frontend/src/index.css` and `frontend/tailwind.config.js` to use different colors.

### 🚀 Deploy
See main README.md for deployment instructions.

---

## API Documentation

Once backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## Troubleshooting

**Backend won't start?**
```bash
# Check if port 8000 is in use
# Or specify a different port:
python main.py --port 8001
```

**"Module not found" error?**
```bash
# Make sure venv is activated and requirements are installed
pip install -r requirements.txt
```

**Frontend can't connect?**
- Check that backend is running
- Make sure frontend `.env` has: `REACT_APP_API_URL=http://localhost:8000`
- Restart frontend with: `npm start`

---

## Test the App

1. Visit http://localhost:3000
2. Click "New Chat"
3. Try asking: "Tell me about Sujan's experience"
4. Use "Download CV" button
5. Share a conversation!

---

Happy coding! 🎉
