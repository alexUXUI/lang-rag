"""
Document processing workflow module.
This module handles the document processing pipeline including text extraction, chunking, and summarization.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from ..common.types import DocumentState
from ..config.settings import llm, document_summary_prompt
from .extractor import extract_text_from_pdf

def build_document_graph() -> StateGraph:
    """
    Build the document processing workflow graph.
    
    Returns:
        StateGraph: The configured document processing workflow
    """
    workflow = StateGraph(DocumentState)
    
    def extract_text(state: DocumentState) -> Dict[str, Any]:
        """Extract text from PDF and split into chunks."""
        try:
            print(f"Extracting text from {state['pdf_path']}...")
            chunks = extract_text_from_pdf(state["pdf_path"])
            return {"chunks": chunks}
        except Exception as e:
            return {"error": str(e)}
    
    def summarize_chunks(state: DocumentState) -> Dict[str, Any]:
        """Generate summaries for each chunk of text."""
        try:
            summaries = []
            for i, chunk in enumerate(state["chunks"]):
                print(f"Summarizing chunk {i+1}/{len(state['chunks'])}...")
                summary = llm.invoke(document_summary_prompt.format(text=chunk))
                summaries.append(summary)
            return {"summaries": summaries}
        except Exception as e:
            return {"error": str(e)}
    
    def combine_summaries(state: DocumentState) -> Dict[str, Any]:
        """Combine individual chunk summaries into a final summary."""
        try:
            if len(state["summaries"]) == 1:
                final_summary = state["summaries"][0]
            else:
                combined_summaries = "\n\n".join(state["summaries"])
                final_prompt = f"Combine these summaries into a coherent overall summary:\n\n{combined_summaries}"
                final_summary = llm.invoke(final_prompt)
            return {"final_summary": final_summary}
        except Exception as e:
            return {"error": str(e)}
    
    def router(state: DocumentState) -> str:
        """Route the workflow based on current state."""
        if "error" in state and state["error"]:
            return "end"
        if "chunks" in state and state["chunks"]:
            if "summaries" not in state or not state["summaries"]:
                return "summarize_chunks"
            if "final_summary" not in state or not state["final_summary"]:
                return "combine_summaries"
        return "end"
    
    # Add nodes to the workflow
    workflow.add_node("extract_text", extract_text)
    workflow.add_node("summarize_chunks", summarize_chunks)
    workflow.add_node("combine_summaries", combine_summaries)
    
    # Add edges to the workflow
    for node in ["extract_text", "summarize_chunks", "combine_summaries"]:
        workflow.add_conditional_edges(
            node,
            router,
            {
                "extract_text": "extract_text",
                "summarize_chunks": "summarize_chunks",
                "combine_summaries": "combine_summaries",
                "end": END
            }
        )
    
    workflow.set_entry_point("extract_text")
    return workflow.compile() 