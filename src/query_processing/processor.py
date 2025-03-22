"""
Query processing workflow module.
This module handles the processing of user queries including spell checking, decomposition, and improvement.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from ..common.types import QueryState
from ..config.settings import llm, spell, spell_check_prompt, decomposition_prompt, hypothesis_prompt, improvement_prompt

def spell_check_query(state: QueryState) -> Dict[str, Any]:
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
        return {"error": str(e)}

def decompose_query(state: QueryState) -> Dict[str, Any]:
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
        return {"error": str(e)}

def identify_hypotheses(state: QueryState) -> Dict[str, Any]:
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
        return {"error": str(e)}

def improve_query(state: QueryState) -> Dict[str, Any]:
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
        return {"error": str(e)}

def build_query_graph() -> StateGraph:
    """
    Build the query processing workflow graph.
    
    Returns:
        StateGraph: The configured query processing workflow
    """
    workflow = StateGraph(QueryState)
    
    def router(state: QueryState) -> str:
        """Route the workflow based on current state."""
        if "error" in state and state["error"]:
            return "end"
        if "query" in state and state["query"]:
            if "spell_checked_query" not in state or not state["spell_checked_query"]:
                return "spell_check_query"
            if "decomposed_queries" not in state or not state["decomposed_queries"]:
                return "decompose_query"
            if "hypotheses" not in state or not state["hypotheses"]:
                return "identify_hypotheses"
            if "improved_query" not in state or not state["improved_query"]:
                return "improve_query"
        return "end"
    
    # Add nodes to the workflow
    workflow.add_node("spell_check_query", spell_check_query)
    workflow.add_node("decompose_query", decompose_query)
    workflow.add_node("identify_hypotheses", identify_hypotheses)
    workflow.add_node("improve_query", improve_query)
    
    # Add edges to the workflow
    for node in ["spell_check_query", "decompose_query", "identify_hypotheses", "improve_query"]:
        workflow.add_conditional_edges(
            node,
            router,
            {
                "spell_check_query": "spell_check_query",
                "decompose_query": "decompose_query",
                "identify_hypotheses": "identify_hypotheses",
                "improve_query": "improve_query",
                "end": END
            }
        )
    
    workflow.set_entry_point("spell_check_query")
    return workflow.compile() 