from fastapi import APIRouter, WebSocket, HTTPException, WebSocketDisconnect
from ..models.chat import ChatRequest, ChatResponse, ChatMessage
from ..core.config import logger
from ..services.session import session_manager
from typing import Dict, Any
import json

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat query and return the response."""
    try:
        if not request.session_id:
            raise HTTPException(status_code=400, detail="Missing session_id")
            
        session = session_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=400, detail="Invalid session_id")
            
        qa_chain = session.get("qa_chain")
        if not qa_chain:
            raise HTTPException(status_code=400, detail="No QA chain initialized for this session")
            
        result = qa_chain({"question": request.query})
        
        return ChatResponse(
            response=result["answer"],
            session_id=request.session_id,
            context="\n".join([doc.page_content for doc in result["source_documents"]])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat."""
    logger.info(f"WebSocket connection attempt for session {session_id}")
    
    session = session_manager.get_session(session_id)
    if not session:
        logger.error(f"Invalid session {session_id}")
        await websocket.close(code=4003, reason="Invalid session")
        return
        
    qa_chain = session.get("qa_chain")
    if not qa_chain:
        logger.error(f"No QA chain found for session {session_id}")
        await websocket.close(code=4003, reason="No QA chain initialized")
        return
        
    await websocket.accept()
    logger.info(f"WebSocket connection accepted for session {session_id}")
    
    try:
        while True:
            logger.info(f"Waiting for message in session {session_id}")
            data = await websocket.receive_json()
            query = data.get("query")
            
            if not query:
                logger.warning("No query provided")
                await websocket.send_json({
                    "error": "No query provided",
                    "response": "",
                    "sources": []
                })
                continue
                
            logger.info(f"Processing query in session {session_id}: {query}")
            try:
                result = qa_chain({"question": query})
                answer = result["answer"]
                sources = [doc.page_content for doc in result["source_documents"]]
                
                logger.info(f"Sending response for session {session_id}")
                response_data = {
                    "response": answer,
                    "sources": sources
                }
                logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
                await websocket.send_json(response_data)
            except Exception as e:
                logger.error(f"Error processing query in session {session_id}: {str(e)}")
                await websocket.send_json({
                    "error": f"Error processing query: {str(e)}",
                    "response": "",
                    "sources": []
                })
                
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error in session {session_id}: {str(e)}")
        try:
            await websocket.send_json({
                "error": f"WebSocket error: {str(e)}",
                "response": "",
                "sources": []
            })
        except:
            pass 