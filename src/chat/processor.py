"""
Chat processing workflow module.
This module handles the chat system including context management, response generation, and history tracking.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from ..common.types import ChatState
from ..config.settings import llm, embeddings, chat_prompt

def build_chat_graph() -> StateGraph:
    """
    Build the chat processing workflow graph.
    
    Returns:
        StateGraph: The configured chat processing workflow
    """
    workflow = StateGraph(ChatState)
    
    def process_chat_question(state: ChatState) -> Dict[str, Any]:
        """Process a chat question and generate a response."""
        try:
            if not state.get("chunks"):
                return {"error": "No document chunks available"}
            
            # Create vector store from chunks
            vectorstore = FAISS.from_texts(
                state["chunks"],
                embeddings,
                metadatas=[{"source": f"chunk_{i}"} for i in range(len(state["chunks"]))]
            )
            
            # Initialize conversation memory
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer",
                input_key="question"
            )
            
            # Create the conversational chain
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
                ),
                memory=memory,
                return_source_documents=True,
                verbose=True,
                combine_docs_chain_kwargs={"prompt": chat_prompt}
            )
            
            # Process the query
            result = chain.invoke({"question": state["query"]})
            
            # Format the response
            response = result["answer"]
            sources = [doc.page_content for doc in result["source_documents"]]
            
            # Update chat history
            if not state.get("chat_history"):
                state["chat_history"] = []
            
            state["chat_history"].append({
                "role": "user",
                "content": state["query"]
            })
            
            state["chat_history"].append({
                "role": "assistant",
                "content": response
            })
            
            # Store enhanced context
            context = f"Document Summary:\n{state['summary']}\n\n"
            context += "Relevant FAQs:\n"
            for faq in state["faqs"]:
                context += f"Q: {faq['question']}\nA: {faq['answer']}\n\n"
            context += "\nRelevant Document Chunks:\n" + "\n\n".join(sources)
            
            return {
                "current_chat_response": response,
                "chat_history": state["chat_history"],
                "context": context
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def router(state: ChatState) -> str:
        """Route the workflow based on current state."""
        if "error" in state and state["error"]:
            return "end"
        if "query" in state and state["query"] and not state.get("current_chat_response"):
            return "process_chat_question"
        return "end"
    
    # Add nodes to the workflow
    workflow.add_node("process_chat_question", process_chat_question)
    
    # Add edges to the workflow
    workflow.add_conditional_edges(
        "process_chat_question",
        router,
        {
            "process_chat_question": "process_chat_question",
            "end": END
        }
    )
    
    workflow.set_entry_point("process_chat_question")
    return workflow.compile() 