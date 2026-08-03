"""
Lore - Router
Decides which tool (if any) a question needs, using a dedicated classification prompt.
"""

import json
import ollama

from src.agent.tools import TOOLS

ROUTER_MODEL = "llama3"


def build_router_prompt(question):
    tool_descriptions = "\n".join(
        f'- "{name}": {info["description"]}' for name, info in TOOLS.items()
    )

    return f"""You are a routing assistant. Decide which tool, if any, should handle the user's question.

Available tools:
{tool_descriptions}

Respond with ONLY a JSON object, no other text, in this exact format:
{{"tool": "<tool name or 'none'>", "args": {{...}}}}

For "search_knowledge", args should be: {{"query": "<the question or key topic>"}}
For "search_movies", args should be: {{"keyword": "<movie title or franchise>", "min_rating": <number or null>}}
If no tool is needed (greetings, small talk, general questions), respond with: {{"tool": "none", "args": {{}}}}

Question: {question}
"""


def decide_action(question):
    """Ask the model which tool to use, and return (tool_name, args). Defaults safely on failure."""
    prompt = build_router_prompt(question)

    response = ollama.chat(
        model=ROUTER_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response["message"]["content"].strip()

    try:
        # Models sometimes wrap JSON in code fences despite instructions - strip them defensively
        raw = raw.replace("```json", "").replace("```", "").strip()
        decision = json.loads(raw)
        tool = decision.get("tool", "none")
        args = decision.get("args", {})

        if tool not in TOOLS and tool != "none":
            return "none", {}

        return tool, args

    except (json.JSONDecodeError, AttributeError):
        # Safe fallback: if we can't parse the router's decision, default to knowledge search
        return "search_knowledge", {"query": question}