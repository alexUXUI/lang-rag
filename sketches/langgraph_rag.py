from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
import fitz  # PyMuPDF
from langchain.prompts import PromptTemplate
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables from .env file
load_dotenv()

# Define our state type
class AgentState(TypedDict):
    messages: Sequence[HumanMessage | AIMessage]
    pdf_path: str
    chunks: List[str]
    summaries: List[str]
    final_summary: str | None

# Use locally running Ollama model
llm = OllamaLLM(
    model="llama3",
    temperature=0.1,
    max_tokens=1024,
    stop=["Observation:", "\nObservation"]
)

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

# Define our graph nodes
def extract_text(state: AgentState) -> Dict[str, Any]:
    """Extract text from PDF and split into chunks."""
    print(f"Extracting text from {state['pdf_path']}...")
    chunks = extract_text_from_pdf(state["pdf_path"])
    return {"chunks": chunks}

def summarize_chunks(state: AgentState) -> Dict[str, Any]:
    """Summarize each chunk of text."""
    summaries = []
    for i, chunk in enumerate(state["chunks"]):
        print(f"Summarizing chunk {i+1}/{len(state['chunks'])}...")
        summary = llm.invoke(prompt_template.format(text=chunk))
        summaries.append(summary)
    return {"summaries": summaries}

def combine_summaries(state: AgentState) -> Dict[str, Any]:
    """Combine all chunk summaries into a final summary."""
    if len(state["summaries"]) == 1:
        final_summary = state["summaries"][0]
    else:
        combined_summaries = "\n\n".join(state["summaries"])
        final_prompt = f"Combine these summaries into a coherent overall summary:\n\n{combined_summaries}"
        final_summary = llm.invoke(final_prompt)
    return {"final_summary": final_summary}

def should_continue(state: AgentState) -> str:
    """Determine if we should continue processing or end."""
    return "end" if "final_summary" in state and state["final_summary"] else "continue"

# Create the graph
def build_rag_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("extract_text", extract_text)
    workflow.add_node("summarize_chunks", summarize_chunks)
    workflow.add_node("combine_summaries", combine_summaries)
    
    # Add edges
    workflow.add_edge("extract_text", "summarize_chunks")
    workflow.add_edge("summarize_chunks", "combine_summaries")
    workflow.add_conditional_edges(
        "combine_summaries",
        should_continue,
        {
            "continue": "extract_text",  # Loop back if needed
            "end": END  # Special end state
        }
    )
    
    # Set entry point
    workflow.set_entry_point("extract_text")
    
    # Compile the graph
    return workflow.compile()

# Function to process a PDF
def process_pdf(pdf_path: str) -> str:
    """Process a PDF file and return its summary."""
    # Build the graph
    chain = build_rag_graph()
    
    # Initialize state
    initial_state = {
        "messages": [],
        "pdf_path": pdf_path,
        "chunks": [],
        "summaries": [],
        "final_summary": None
    }
    
    try:
        # Execute the graph
        print(f"Processing PDF: {pdf_path}")
        final_state = chain.invoke(initial_state)
        return final_state["final_summary"]
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

# Run the process
if __name__ == "__main__":
    pdf_path = "./test.pdf"
    summary = process_pdf(pdf_path)
    if summary:
        print("\nSummary:")
        print(summary)
    else:
        print("Failed to generate summary")