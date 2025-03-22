from fastapi import APIRouter, HTTPException
from ..models.session import SessionData, SessionState
from ..services.pdf import extract_text_from_pdf
from ..services.qa import initialize_qa_chain
from ..services.session import session_manager
from ..core.config import logger
from typing import Dict, Any

router = APIRouter()

@router.post("/sessions/{session_id}")
async def create_session(session_id: str, session_data: SessionData):
    """Create a new session with the given PDF path"""
    try:
        # Initialize session data
        session = SessionState(
            pdf_path=session_data.pdf_path,
            qa_chain=None,
            summary=None,
            faqs=None
        )
        
        # Only process PDF if path is provided
        if session_data.pdf_path:
            # Extract text from PDF
            text = extract_text_from_pdf(session_data.pdf_path)
            
            # Generate summary and FAQs
            summary = "Document summary will be generated here"  # Placeholder for now
            faqs = []  # Placeholder for now
            
            # Create QA chain
            qa_chain, document_state = initialize_qa_chain([text], summary, faqs)
            
            # Update session data
            session.qa_chain = qa_chain
            session.summary = summary
            session.faqs = faqs
        
        # Store session data
        session_manager.create_session(session_id, session)
        return {"session_id": session_id, "status": "created"}
    except Exception as e:
        logger.error(f"Error creating session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session."""
    if session_manager.delete_session(session_id):
        return {"message": "Session deleted successfully"}
    raise HTTPException(status_code=404, detail="Session not found") 