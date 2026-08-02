"""
Lore - Assistant Core
Shared RAG logic used by both the CLI and the Streamlit UI.
"""

import ollama

from src.rag.retriever import get_relevant_documents
from src.rag.prompt import build_prompt

CHAT_MODEL = "llama3"

SYSTEM_PROMPT = """You are Lore, a local AI assistant that helps users explore fictional worlds, characters, and stories.
Answer using the provided context when available. If the context doesn't cover the question, say so honestly rather than guessing.
Keep answers clear, concise, and conversational."""


def ask_ai(question, conversation_history):
    """Retrieve relevant knowledge, build a grounded prompt, and get the AI's answer."""
    retrieved_docs = get_relevant_documents(question)
    prompt = build_prompt(question, retrieved_docs)

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + conversation_history
        + [{"role": "user", "content": prompt}]
    )

    response = ollama.chat(model=CHAT_MODEL, messages=messages)
    answer = response["message"]["content"]

    conversation_history.append({"role": "user", "content": question})
    conversation_history.append({"role": "assistant", "content": answer})
    conversation_history[:] = conversation_history[-20:]

    sources = [doc["source"] for doc in retrieved_docs]
    return answer, sources