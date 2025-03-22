from typing import List, Dict, Optional, Any, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

def initialize_qa_chain(
    documents: List[str],
    summary: Optional[str] = None,
    faqs: Optional[List[Dict[str, str]]] = None
) -> Tuple[Any, Dict[str, Any]]:
    """Initialize the QA chain with the provided documents."""
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Split documents into chunks
    splits = text_splitter.create_documents(documents)
    
    # Create vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(splits, embeddings)
    
    # Initialize memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Create custom prompt template
    custom_prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template="""You are a helpful assistant specialized in regulatory compliance. Use the following context and chat history to answer the current question.

Context:
{context}

Chat History:
{chat_history}

Current Question: {question}

Instructions:
1. First, check if the answer can be found in the provided context
2. If not, look for relevant information in the document chunks
3. If still not found, say so explicitly
4. Always cite the source of your information
5. Provide clear, accurate answers based on the regulatory context
6. If you find multiple relevant pieces of information, combine them into a comprehensive response

Provide a clear, accurate answer based on the regulatory context."""
    )
    
    # Create QA chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0),
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        ),
        memory=memory,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    
    return qa_chain, {
        "chunks": documents,
        "summary": summary,
        "faqs": faqs
    } 