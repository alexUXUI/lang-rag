"""
Configuration settings and model initialization for the application.
This module contains all the global settings, model configurations, and prompt templates.
"""

from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from spellchecker import SpellChecker

# Load environment variables
load_dotenv()

# Initialize LLM with optimized parameters
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

# Prompt templates for different processing steps
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

# Document processing prompts
document_summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text:\n\n{text}"
)

# FAQ generation prompts
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

# Chat system prompts
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

# Example questions for testing
EXAMPLE_QUESTIONS = [
    "What are the key requirements for compliance with this regulation?",
    "Are there any specific exemptions or exceptions mentioned?",
    "What are the main technical specifications that need to be met?",
    "How does this regulation compare to similar standards?",
    "What are the potential challenges in implementing these requirements?"
] 