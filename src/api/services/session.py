from typing import Dict, Any, Optional
from ..models.session import SessionState
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages active chat sessions."""
    
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._qa_chains: Dict[str, Any] = {}  # Store QA chains separately
    
    def create_session(self, session_id: str, session_data: SessionState) -> None:
        """Create a new session."""
        # Store QA chain separately if it exists
        if session_data.qa_chain is not None:
            self._qa_chains[session_id] = session_data.qa_chain
        
        # Store session data without the QA chain
        session_dict = session_data.dict()
        session_dict.pop('qa_chain', None)  # Remove QA chain from session data
        self._sessions[session_id] = session_dict
        logger.info(f"Created new session: {session_id}")
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a session by ID."""
        session_data = self._sessions.get(session_id)
        if session_data:
            # Add QA chain back to session data if it exists
            if session_id in self._qa_chains:
                session_data['qa_chain'] = self._qa_chains[session_id]
        return session_data
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            self._qa_chains.pop(session_id, None)  # Remove QA chain if it exists
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> None:
        """Update session data."""
        if session_id in self._sessions:
            # Handle QA chain separately if it's in the update data
            if 'qa_chain' in session_data:
                self._qa_chains[session_id] = session_data.pop('qa_chain')
            
            self._sessions[session_id].update(session_data)
            logger.info(f"Updated session: {session_id}")

# Create a global session manager instance
session_manager = SessionManager() 