# Basic RAG (Retrieval Augmented Generation) API

A FastAPI-based service that provides document processing, question answering, and real-time chat capabilities using RAG (Retrieval Augmented Generation) techniques. The service can process PDF documents, generate FAQs, and provide interactive chat sessions with context-aware responses.

## Features

- PDF document processing and text extraction
- Document chunking and vector storage
- FAQ generation from documents
- Real-time WebSocket chat interface
- Session management for multiple chat instances
- Context-aware responses using RAG
- Interactive web interface for testing

## Prerequisites

- Python 3.8+
- Ollama (for local LLM support)
- OpenAI API key (for embeddings)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd basic-rag
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_api_key
```

## Project Structure

```
basic-rag/
├── src/
│   ├── api/                 # API implementation
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Pydantic models
│   │   ├── routes/         # API routes
│   │   └── services/       # API-specific services
│   ├── services/           # Core intelligent services
│   │   ├── chat/          # Chat functionality
│   │   ├── common/        # Shared utilities
│   │   ├── config/        # Configuration management
│   │   ├── document_processing/  # PDF and text processing
│   │   ├── faq_generation/      # FAQ generation logic
│   │   └── query_processing/    # Query handling and RAG
│   ├── static/             # Static files (HTML, CSS)
│   └── main.py             # Main application entry
├── tests/                  # Test files
├── data/                   # Data directory for PDFs
├── requirements.txt        # Main dependencies
└── requirements-test.txt   # Test dependencies
```

## Running the API

1. Start the FastAPI server:
```bash
# From the project root directory
python run.py
```

The server will start at `http://localhost:8000`

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

3. Test the WebSocket interface:
- Open `http://localhost:8000/static/test.html` in your browser
- Create a session with a PDF file
- Connect to the WebSocket
- Start chatting with the document

## API Endpoints

### HTTP Endpoints

- `POST /sessions/{session_id}`: Create a new chat session
- `DELETE /sessions/{session_id}`: Delete a chat session
- `POST /chat`: Send a chat message (HTTP)
- `POST /upload`: Upload a PDF document
- `POST /faq`: Generate FAQs from a document

### WebSocket Endpoint

- `ws://localhost:8000/ws/chat/{session_id}`: WebSocket connection for real-time chat

## Running Tests

1. Install test dependencies:
```bash
pip install -r tests/requirements-test.txt
```

2. Run the test suite:
```bash
python tests/test_websocket.py
```

## Development

### Running Services Independently

To run specific services for development or testing:

1. Document Processing:
```bash
python -m src.services.document_processing.processor
```

2. FAQ Generation:
```bash
python -m src.services.faq_generation.processor
```

3. Chat Service:
```bash
python -m src.services.chat.processor
```

### Adding New Features

1. Create new models in `src/api/models/`
2. Add business logic in `src/services/` (for core services) or `src/api/services/` (for API-specific services)
3. Create new routes in `src/api/routes/`
4. Update tests in the `tests/` directory

### Code Style

The project follows PEP 8 guidelines. Use a code formatter like `black` for consistent formatting:

```bash
pip install black
black src/ tests/
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Issues**
   - Ensure the server is running
   - Check if the session ID is valid
   - Verify the PDF file exists and is accessible

2. **PDF Processing Errors**
   - Check if the PDF file is not corrupted
   - Verify file permissions
   - Ensure the file path is correct

3. **API Key Issues**
   - Verify your OpenAI API key is set in `.env`
   - Check if the key is valid and has sufficient credits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.