import asyncio
import websockets
import json
import requests
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoints
BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/chat"

async def test_websocket_chat():
    """Test the WebSocket chat functionality."""
    try:
        # Step 1: Create a test session
        session_id = "test_session_123"
        pdf_path = "./data/test.pdf"  # Make sure this file exists
        
        # Create session
        response = requests.post(
            f"{BASE_URL}/sessions/{session_id}",
            json={"pdf_path": pdf_path}
        )
        response.raise_for_status()
        logger.info(f"Created session: {session_id}")
        
        # Give the server a moment to process the PDF
        time.sleep(2)
        
        # Step 2: Connect to WebSocket
        ws_url = f"{WS_URL}/{session_id}"
        logger.info(f"Connecting to WebSocket: {ws_url}")
        
        async with websockets.connect(ws_url) as websocket:
            # Step 3: Send a test query
            test_query = "What is this document about?"
            logger.info(f"Sending query: {test_query}")
            
            await websocket.send(json.dumps({"query": test_query}))
            
            # Step 4: Receive and verify response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            logger.info("Received response:")
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            
            # Check for errors
            if "error" in response_data and response_data["error"]:
                raise Exception(f"Server returned error: {response_data['error']}")
            
            # Verify response structure
            assert "response" in response_data, "Response missing 'response' field"
            assert "sources" in response_data, "Response missing 'sources' field"
            assert response_data["response"], "Response is empty"
            
            # Step 5: Send another query to test conversation context
            follow_up_query = "Can you provide more details about the main requirements?"
            logger.info(f"Sending follow-up query: {follow_up_query}")
            
            await websocket.send(json.dumps({"query": follow_up_query}))
            response = await websocket.recv()
            response_data = json.loads(response)
            
            logger.info("Received follow-up response:")
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            
            # Check for errors in follow-up response
            if "error" in response_data and response_data["error"]:
                raise Exception(f"Server returned error in follow-up: {response_data['error']}")
            
        # Step 6: Clean up - delete the session
        response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
        response.raise_for_status()
        logger.info(f"Deleted session: {session_id}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_websocket_chat()) 