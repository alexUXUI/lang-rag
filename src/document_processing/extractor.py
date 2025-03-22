"""
PDF text extraction module.
This module handles the extraction and chunking of text from PDF documents.
"""

import fitz  # PyMuPDF
from typing import List

def extract_text_from_pdf(pdf_path: str, max_chars_per_chunk: int = 4000) -> List[str]:
    """
    Extract text from a PDF file and split it into manageable chunks.
    
    Args:
        pdf_path (str): Path to the PDF file
        max_chars_per_chunk (int): Maximum number of characters per chunk
        
    Returns:
        List[str]: List of text chunks extracted from the PDF
    """
    doc = fitz.open(pdf_path)
    print(f"Number of pages in PDF: {doc.page_count}")
    chunks = []
    current_chunk = ""
    
    for page in doc:
        print(f"Extracting text from page {page.number + 1}...")
        page_text = page.get_text()
        
        if len(current_chunk) + len(page_text) > max_chars_per_chunk:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = page_text
        else:
            current_chunk += page_text
    
    if current_chunk:
        chunks.append(current_chunk)
        
    print(f"Split PDF into {len(chunks)} chunks")
    return chunks 