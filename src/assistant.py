"""
Lore - Assistant Core
Shared AI logic used by both the CLI and the Streamlit UI.
"""

import ollama

from src.config import CHAT_MODEL, MAX_HISTORY_MESSAGES
from src.agent.router import decide_action
from src.agent.tools import TOOLS

SYSTEM_PROMPT = """You are Lore, a local AI assistant that helps users explore fictional worlds, characters, and stories.
Answer using the provided context when available. If the context doesn't cover the question, say so honestly rather than guessing.
Keep answers clear, concise, and conversational."""


def ask_ai(question, conversation_history):
    """
    Route the question to the appropriate tool (if any),
    then use the LLM to generate a grounded response.
    """
    tool_name, args = decide_action(question)

    if tool_name == "none":
        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + conversation_history
            + [{"role": "user", "content": question}]
        )

        response = ollama.chat(
            model=CHAT_MODEL,
            messages=messages,
        )

        answer = response["message"]["content"]
        sources = []

    else:
        tool_context, sources = TOOLS[tool_name]["run"](args)

        prompt = f"""Use the following information to answer the user's question.

If the information is insufficient, say so honestly.
Do not invent facts.

Information:
{tool_context}

Question:
{question}
"""

        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + conversation_history
            + [{"role": "user", "content": prompt}]
        )

        response = ollama.chat(
            model=CHAT_MODEL,
            messages=messages,
        )

        answer = response["message"]["content"]

    conversation_history.append({"role": "user", "content": question})
    conversation_history.append({"role": "assistant", "content": answer})
    conversation_history[:] = conversation_history[-MAX_HISTORY_MESSAGES:]

    return answer, sources, tool_name