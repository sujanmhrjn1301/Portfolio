"""
api.py
FastAPI backend for Lexi Legal Assistant (headless API).

- POST /api/v1/ask
- CORS enabled for https://sujanmaharjan5.com.np
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

# CORS settings
origins = [
    "https://sujanmaharjan5.com.np"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
