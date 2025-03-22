from fastapi import APIRouter, File, UploadFile, HTTPException
from ..services.pdf import extract_text_from_pdf
from ..services.qa import initialize_qa_chain
from ..core.config import logger
from typing import Dict
import tempfile
import json

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document and process it."""
    try:
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Process the PDF
            text = extract_text_from_pdf(temp_file.name)
            qa_chain, document_state = initialize_qa_chain([text])
            
            return {
                "message": "Document processed successfully",
                "text": text,
                "temp_path": temp_file.name
            }
            
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/faq")
async def generate_faq(data: Dict[str, str]):
    """Generate FAQs from a document."""
    try:
        logger.info("Generating FAQs for document")
        pdf_path = data.get("pdf_path")
        if not pdf_path:
            raise HTTPException(status_code=400, detail="PDF path is required")
            
        logger.info(f"Processing PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        
        # Initialize QA chain for FAQ generation
        qa_chain, _ = initialize_qa_chain([text])
        
        # Generate FAQs using the QA chain
        faq_prompt = """Based on the following document content, generate 5 frequently asked questions (FAQs) that would be most relevant for users trying to understand this document. For each FAQ, provide a clear and concise answer.

Document Content:
{context}

Please format the response as a JSON array of objects with 'question' and 'answer' fields."""
        
        # Get FAQs from QA chain
        result = qa_chain({"question": faq_prompt})
        faqs = result["answer"]
        
        # Try to parse the JSON response
        try:
            faqs = json.loads(faqs)
        except json.JSONDecodeError:
            # If parsing fails, create a simple FAQ structure
            faqs = [{"question": "What is this document about?", "answer": "This document appears to be a technical specification or regulatory document."}]
        
        logger.info(f"Generated {len(faqs)} FAQs")
        return {"faqs": faqs}
        
    except Exception as e:
        logger.error(f"Error generating FAQs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 