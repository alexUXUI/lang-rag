from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
import fitz  # PyMuPDF
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain.agents import Tool, AgentExecutor, AgentType, initialize_agent
from langchain.schema import HumanMessage
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import Graph, StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import BaseTool

# Load environment variables from .env file
load_dotenv()

# Define our state type
class AgentState(TypedDict):
    messages: Sequence[HumanMessage | AIMessage]
    pdf_path: str
    chunks: list[str]
    summaries: list[str]
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

# Create a runnable sequence for summarization
summarization_chain = prompt_template | llm

# Define our graph nodes
def extract_text(state: AgentState) -> AgentState:
    """Extract text from PDF and split into chunks."""
    chunks = extract_text_from_pdf(state["pdf_path"])
    return {"**state": state, "chunks": chunks}

def summarize_chunks(state: AgentState) -> AgentState:
    """Summarize each chunk of text."""
    summaries = []
    for i, chunk in enumerate(state["chunks"]):
        print(f"Summarizing chunk {i+1}/{len(state['chunks'])}...")
        summary = summarization_chain.invoke({"text": chunk})
        summaries.append(summary)
    return {"**state": state, "summaries": summaries}

def combine_summaries(state: AgentState) -> AgentState:
    """Combine all chunk summaries into a final summary."""
    if len(state["summaries"]) == 1:
        final_summary = state["summaries"][0]
    else:
        combined_summaries = "\n\n".join(state["summaries"])
        final_prompt = f"Combine these summaries into a coherent overall summary:\n\n{combined_summaries}"
        final_summary = llm.invoke(final_prompt)
    return {"**state": state, "final_summary": final_summary}

def should_continue(state: AgentState) -> AgentState:
    """Determine if we should continue processing."""
    return {"**state": state}

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("extract_text", extract_text)
workflow.add_node("summarize_chunks", summarize_chunks)
workflow.add_node("combine_summaries", combine_summaries)
workflow.add_node("should_continue", should_continue)

# Add edges
workflow.add_edge("extract_text", "summarize_chunks")
workflow.add_edge("summarize_chunks", "combine_summaries")
workflow.add_edge("combine_summaries", "should_continue")

# Add conditional edges from should_continue
workflow.add_conditional_edges(
    "should_continue",
    lambda x: "end" if x["final_summary"] else "continue",
    {
        "end": END,  # End the graph
        "continue": "combine_summaries"  # Loop back to combine_summaries if needed
    }
)

# Set entry point
workflow.set_entry_point("extract_text")

# Compile the graph
chain = workflow.compile()

# Function to process a PDF
def process_pdf(pdf_path: str) -> str:
    """Process a PDF file and return its summary."""
    initial_state = {
        "messages": [],
        "pdf_path": pdf_path,
        "chunks": [],
        "summaries": [],
        "final_summary": None
    }
    
    try:
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
        print("Summary:", summary)
    else:
        print("Failed to generate summary")