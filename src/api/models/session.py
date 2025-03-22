from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class SessionData(BaseModel):
    pdf_path: Optional[str] = None

class SessionState(BaseModel):
    pdf_path: Optional[str] = None
    qa_chain: Optional[Any] = None
    summary: Optional[str] = None
    faqs: Optional[List[Dict[str, str]]] = None 