from fastapi.responses import FileResponse
from .core.config import app
from .routes import chat, documents, sessions

# Include routers
app.include_router(chat.router, tags=["chat"])
app.include_router(documents.router, tags=["documents"])
app.include_router(sessions.router, tags=["sessions"])

@app.get("/")
async def read_root():
    """Serve the chat interface."""
    return FileResponse("src/static/index.html") 