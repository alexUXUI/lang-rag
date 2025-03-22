"""
FAQ generation workflow module.
This module handles the generation of FAQs from document chunks.
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from ..common.types import FAQState
from ..config.settings import llm, faq_generation_prompt

def build_faq_graph() -> StateGraph:
    """
    Build the FAQ generation workflow graph.
    
    Returns:
        StateGraph: The configured FAQ generation workflow
    """
    workflow = StateGraph(FAQState)
    
    def generate_faqs(state: FAQState) -> Dict[str, Any]:
        """Generate FAQs from document chunks."""
        try:
            if not state.get("chunks"):
                return {"error": "No document chunks available"}
                
            faqs = []
            for i, chunk in enumerate(state["chunks"]):
                print(f"Generating FAQs for chunk {i+1}/{len(state['chunks'])}...")
                section_title = chunk.split('\n')[0][:100] if chunk else "Section"
                faq_result = llm.invoke(faq_generation_prompt.format(
                    text=chunk,
                    section_title=section_title
                ))
                
                current_faqs = []
                current_question = None
                current_answer = []
                
                for line in faq_result.split('\n'):
                    if line.startswith('Q:'):
                        if current_question and current_answer:
                            current_faqs.append({
                                "question": current_question,
                                "answer": "\n".join(current_answer)
                            })
                        current_question = line[2:].strip()
                        current_answer = []
                    elif line.startswith('A:'):
                        current_answer.append(line[2:].strip())
                    elif current_answer is not None:
                        current_answer.append(line.strip())
                
                if current_question and current_answer:
                    current_faqs.append({
                        "question": current_question,
                        "answer": "\n".join(current_answer)
                    })
                
                faqs.extend(current_faqs)
            
            return {"faqs": faqs}
        except Exception as e:
            return {"error": str(e)}
    
    def router(state: FAQState) -> str:
        """Route the workflow based on current state."""
        if "error" in state and state["error"]:
            return "end"
        if "chunks" in state and state["chunks"] and ("faqs" not in state or not state["faqs"]):
            return "generate_faqs"
        return "end"
    
    # Add nodes to the workflow
    workflow.add_node("generate_faqs", generate_faqs)
    
    # Add edges to the workflow
    workflow.add_conditional_edges(
        "generate_faqs",
        router,
        {
            "generate_faqs": "generate_faqs",
            "end": END
        }
    )
    
    workflow.set_entry_point("generate_faqs")
    return workflow.compile() 