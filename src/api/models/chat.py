from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    context: Optional[str] = None

class ChatMessage(BaseModel):
    query: str
    response: Optional[str] = None
    sources: Optional[List[str]] = None
    error: Optional[str] = None 