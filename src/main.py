"""
Main orchestrator module.
This module coordinates the document processing, FAQ generation, and chat functionality.
"""

from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
import fitz  # PyMuPDF
from langchain.prompts import PromptTemplate
from typing import TypedDict, Annotated, Sequence, List, Dict, Any, Optional, Union
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import traceback
from spellchecker import SpellChecker
import re
from .document_processing.processor import build_document_graph
from .faq_generation.processor import build_faq_graph
from .chat.processor import build_chat_graph
from .config.settings import EXAMPLE_QUESTIONS

# Load environment variables from .env file
load_dotenv()

# Define our state type with proper typing
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

# Use locally running Ollama model with optimized parameters
llm = OllamaLLM(
    model="llama3",
    temperature=0.1,
    max_tokens=1024,
    stop=["Observation:", "\nObservation"]
)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize spell checker
spell = SpellChecker()

# Prompt templates for different query processing steps
spell_check_prompt = PromptTemplate(
    input_variables=["query"],
    template="""Review the following query for spelling and grammar errors:
Query: {query}

Provide the corrected query with proper spelling and grammar."""
)

decomposition_prompt = PromptTemplate(
    input_variables=["query"],
    template="""Decompose the following query into simpler sub-queries:
Query: {query}

Break down complex concepts and provide a list of simpler queries that together cover the original question."""
)

hypothesis_prompt = PromptTemplate(
    input_variables=["query", "decomposed_queries"],
    template="""Based on the following query and its sub-queries, identify key hypotheses:
Original Query: {query}
Sub-queries: {decomposed_queries}

List the main hypotheses that need to be tested or verified."""
)

improvement_prompt = PromptTemplate(
    input_variables=["query", "decomposed_queries", "hypotheses"],
    template="""Improve the following query based on its decomposition and hypotheses:
Original Query: {query}
Sub-queries: {decomposed_queries}
Hypotheses: {hypotheses}

Provide an improved version of the query that is more precise and comprehensive."""
)

# Add new prompt templates for FAQ generation and chat
faq_generation_prompt = PromptTemplate(
    input_variables=["text", "section_title"],
    template="""Generate a list of frequently asked questions (FAQs) for the following section of a regulatory document:

Section Title: {section_title}
Content: {text}

Generate 5-7 relevant FAQs that would help users understand this section better. Format each FAQ as:
Q: [Question]
A: [Answer]

Focus on:
1. Key requirements and specifications
2. Common compliance questions
3. Important technical details
4. Potential implementation challenges
5. Clarifications of complex terms

Provide clear, concise answers based on the content."""
)

chat_prompt = PromptTemplate(
    input_variables=["context", "chat_history", "current_question"],
    template="""You are a helpful assistant specialized in regulatory compliance. Use the following context and chat history to answer the current question:

Context:
{context}

Chat History:
{chat_history}

Current Question: {current_question}

Instructions:
1. First, check if the answer can be found in the FAQs
2. If not, look for relevant information in the document summary
3. If still not found, search through the document content
4. If the answer cannot be found in any of these sources, say so explicitly
5. Always cite the source of your information (FAQs, Summary, or Document Content)

Provide a clear, accurate answer based on the regulatory context. If you find multiple relevant pieces of information, combine them into a comprehensive response."""
)

# Add hardcoded example questions for testing
EXAMPLE_QUESTIONS = [
    "What are the key requirements for compliance with this regulation?",
    "Are there any specific exemptions or exceptions mentioned?",
    "What are the main technical specifications that need to be met?",
    "How does this regulation compare to similar standards?",
    "What are the potential challenges in implementing these requirements?"
]

def spell_check_query(state: DocumentState) -> Dict[str, Any]:
    """Check and correct spelling in the query."""
    try:
        if "error" in state and state["error"]:
            return {}
            
        if not state.get("query"):
            return {"error": "No query provided"}
            
        # Use pyspellchecker for spell checking
        words = state["query"].split()
        misspelled = spell.unknown(words)
        
        # Correct misspelled words
        corrected_words = []
        for word in words:
            if word in misspelled:
                corrected_words.append(spell.correction(word))
            else:
                corrected_words.append(word)
                
        corrected_query = " ".join(corrected_words)
        
        # Use LLM for grammar correction
        grammar_corrected = llm.invoke(spell_check_prompt.format(query=corrected_query))
        
        return {"spell_checked_query": grammar_corrected}
    except Exception as e:
        error_msg = f"Error in spell checking: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return {"error": error_msg}

def decompose_query(state: DocumentState) -> Dict[str, Any]:
    """Decompose the query into simpler sub-queries."""
    try:
        if "error" in state and state["error"]:
            return {}
            
        if not state.get("spell_checked_query"):
            return {"error": "No spell-checked query available"}
            
        # Use LLM for query decomposition
        decomposition_result = llm.invoke(decomposition_prompt.format(query=state["spell_checked_query"]))
        
        # Extract sub-queries from the result
        decomposed_queries = [q.strip() for q in decomposition_result.split('\n') if q.strip()]
        
        return {"decomposed_queries": decomposed_queries}
    except Exception as e:
        error_msg = f"Error in query decomposition: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return {"error": error_msg}

def identify_hypotheses(state: DocumentState) -> Dict[str, Any]:
    """Identify key hypotheses from the query and its decomposition."""
    try:
        if "error" in state and state["error"]:
            return {}
            
        if not state.get("decomposed_queries"):
            return {"error": "No decomposed queries available"}
            
        # Use LLM to identify hypotheses
        hypotheses_result = llm.invoke(hypothesis_prompt.format(
            query=state["spell_checked_query"],
            decomposed_queries="\n".join(state["decomposed_queries"])
        ))
        
        # Extract hypotheses from the result
        hypotheses = [h.strip() for h in hypotheses_result.split('\n') if h.strip()]
        
        return {"hypotheses": hypotheses}
    except Exception as e:
        error_msg = f"Error in hypothesis identification: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return {"error": error_msg}

def improve_query(state: DocumentState) -> Dict[str, Any]:
    """Improve the query based on decomposition and hypotheses."""
    try:
        if "error" in state and state["error"]:
            return {}
            
        if not state.get("hypotheses"):
            return {"error": "No hypotheses available"}
            
        # Use LLM to improve the query
        improved_query = llm.invoke(improvement_prompt.format(
            query=state["spell_checked_query"],
            decomposed_queries="\n".join(state["decomposed_queries"]),
            hypotheses="\n".join(state["hypotheses"])
        ))
        
        return {"improved_query": improved_query}
    except Exception as e:
        error_msg = f"Error in query improvement: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return {"error": error_msg}

# Load PDF and extract text with chunking to prevent overwhelming the LLM
def extract_text_from_pdf(pdf_path: str, max_chars_per_chunk=4000) -> list:
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

# Define a prompt template for summarization
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text:\n\n{text}"
)

def process_pdf(pdf_path: str, query: Optional[str] = None, previous_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process a PDF file and handle any queries about its contents.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        query (Optional[str]): Optional query to process about the document
        previous_state (Optional[Dict[str, Any]]): Previous processing state to reuse
        
    Returns:
        Dict[str, Any]: Processing results including summary, FAQs, and chat responses
    """
    try:
        # Initialize state
        doc_state = {
            "pdf_path": pdf_path,
            "chunks": [],
            "summaries": [],
            "final_summary": None,
            "error": None
        }
        
        # If we have previous state, reuse the document processing results
        if previous_state and previous_state.get("chunks"):
            doc_state["chunks"] = previous_state["chunks"]
            doc_state["summaries"] = previous_state.get("summaries", [])
            doc_state["final_summary"] = previous_state.get("final_summary")
        else:
            # Process document only if we don't have previous state
            doc_graph = build_document_graph()
            doc_result = doc_graph.invoke(doc_state)
            
            if doc_result.get("error"):
                return {"error": doc_result["error"]}
            
            doc_state = doc_result
        
        # Generate FAQs only if we don't have them from previous state
        if not (previous_state and previous_state.get("faqs")):
            faq_state = {
                "chunks": doc_state["chunks"],
                "faqs": None,
                "error": None
            }
            faq_graph = build_faq_graph()
            faq_result = faq_graph.invoke(faq_state)
            
            if faq_result.get("error"):
                return {"error": faq_result["error"]}
            
            faqs = faq_result["faqs"]
        else:
            faqs = previous_state["faqs"]
        
        # If there's a query, process it
        if query:
            # Process chat with enhanced context
            chat_state = {
                "query": query,
                "chunks": doc_state["chunks"],
                "chat_history": previous_state.get("chat_history") if previous_state else [],
                "current_chat_response": None,
                "error": None,
                "summary": doc_state["final_summary"],
                "faqs": faqs
            }
            
            chat_graph = build_chat_graph()
            chat_result = chat_graph.invoke(chat_state)
            
            if chat_result.get("error"):
                return {"error": chat_result["error"]}
            
            return {
                "summary": doc_state["final_summary"],
                "faqs": faqs,
                "chat_history": chat_result["chat_history"],
                "current_chat_response": chat_result["current_chat_response"],
                "chunks": doc_state["chunks"],
                "summaries": doc_state["summaries"]
            }
        
        # If no query, just return document processing results
        return {
            "summary": doc_state["final_summary"],
            "faqs": faqs,
            "chunks": doc_state["chunks"],
            "summaries": doc_state["summaries"]
        }
        
    except Exception as e:
        error_msg = f"Error in processing: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return {"error": error_msg}

def main():
    """Main entry point for the application."""
    pdf_path = "./data/test.pdf"
    
    # First, process the PDF to generate summary and FAQs
    print("Processing PDF for summary and FAQs...")
    result = process_pdf(pdf_path)
    
    # Check for errors in the result
    if result.get("error"):
        print("\nError occurred during processing:")
        print(result["error"])
        return
    
    if result.get("summary"):
        print("\nSummary:")
        print(result["summary"])
    
    if result.get("faqs"):
        print("\nGenerated FAQs:")
        for faq in result["faqs"]:
            print(f"\nQ: {faq['question']}")
            print(f"A: {faq['answer']}")
    
    # Test chat with example questions
    print("\nTesting chat with example questions:")
    
    for question in EXAMPLE_QUESTIONS:
        print(f"\nQuestion: {question}")
        # Pass the entire previous state to ensure all processed data is reused
        chat_result = process_pdf(pdf_path, question, previous_state=result)
        
        if chat_result.get("error"):
            print(f"Error: {chat_result['error']}")
            continue
            
        if chat_result.get("current_chat_response"):
            print(f"Answer: {chat_result['current_chat_response']}")
        else:
            print("Failed to generate response")
            
        # Update result with new chat history for next question
        result = chat_result  # Update the entire state for the next iteration

if __name__ == "__main__":
    main()


        