"""
api.py
FastAPI backend for Lexi Legal Assistant (headless API).

- POST /api/v1/ask
- CORS enabled for Memora portfolio frontend
- Uses core_logic.get_legal_response
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.core_logic import get_legal_response

load_dotenv()

app = FastAPI(title="Lexi Legal Assistant API")

# CORS settings - Allow requests from Memora frontend
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    CORS_ORIGINS = [
        "https://sujanmaharjan5.com.np",  # Production Memora frontend
        os.getenv("LEXI_CORS_ORIGIN", "https://sujanmaharjan5.com.np")  # Explicit override
    ]
else:
    # Development - allow localhost
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only needed methods
    allow_headers=["Content-Type"],
)

class AskRequest(BaseModel):
    query: str
    mode: str

@app.post("/api/v1/ask")
def ask_lexi(request: AskRequest):
    """
    POST endpoint for Lexi legal assistant.
    Request JSON: {"query": ..., "mode": ...}
    Response JSON: {"answer": ..., "metadata": ..., "process_logs": [...]}
    """
    result = get_legal_response(request.query, request.mode)
    return result
