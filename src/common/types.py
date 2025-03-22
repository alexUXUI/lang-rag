"""
Common type definitions used across the application.
These types define the structure of state objects used in various processing pipelines.
"""

from typing import TypedDict, List, Dict, Any, Optional

class DocumentState(TypedDict):
    """State for document processing (extraction, summarization)"""
    pdf_path: str
    chunks: List[str]
    summaries: List[str]
    final_summary: Optional[str]
    error: Optional[str]

class FAQState(TypedDict):
    """State for FAQ generation"""
    chunks: List[str]
    faqs: Optional[List[Dict[str, str]]]
    error: Optional[str]

class QueryState(TypedDict):
    """State for query processing"""
    query: str
    spell_checked_query: Optional[str]
    decomposed_queries: Optional[List[str]]
    hypotheses: Optional[List[str]]
    improved_query: Optional[str]
    error: Optional[str]

class ChatState(TypedDict):
    """State for chat processing"""
    query: str
    chunks: List[str]
    chat_history: Optional[List[Dict[str, str]]]
    current_chat_response: Optional[str]
    error: Optional[str]
    context: Optional[str]
    summary: Optional[str]
    faqs: Optional[List[Dict[str, str]]] 