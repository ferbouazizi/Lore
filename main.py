import ollama

from src.rag.retriever import get_relevant_documents

CHAT_MODEL = "llama3"

SYSTEM_PROMPT = """You are Lore, a local AI assistant that helps users explore fictional worlds, characters, and stories.
Answer using the provided context when available. If the context doesn't cover the question, say so honestly rather than guessing.
Keep answers clear, concise, and conversational."""

def build_prompt(question, retrieved_docs):
    """Combine retrieved knowledge and the user's question into one prompt."""
    context = "\n\n".join(doc["content"] for doc in retrieved_docs)

    prompt = f"""Use the following context to answer the question.
If the context doesn't contain enough information, say so honestly instead of guessing.

Context:
{context}

Question: {question}
"""
    return prompt


def ask_ai(question, conversation_history):
    """
    Retrieve relevant knowledge, combine it with conversation history,
    and generate an AI response.
    """

    retrieved_docs = get_relevant_documents(question)

    prompt = build_prompt(question, retrieved_docs)

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + conversation_history
        + [{"role": "user", "content": prompt}]
    )

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=messages
    )

    answer = response["message"]["content"]

    # Save normal conversation memory
    conversation_history.append(
        {"role": "user", "content": question}
    )

    conversation_history.append(
        {"role": "assistant", "content": answer}
    )

    # Keep only the last 10 exchanges
    conversation_history[:] = conversation_history[-20:]

    sources = [doc["source"] for doc in retrieved_docs]

    return answer, sources


def main():
    print("================================")
    print("Lore")
    print("================================")
    print("Local AI Assistant with RAG")
    print("Type 'exit' to quit.\n")

    conversation_history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer, sources = ask_ai(
            question,
            conversation_history
        )

        print(f"\nLORE: {answer}")

        if sources:
            print(f"(sources: {', '.join(sources)})")

        print()


if __name__ == "__main__":
    main()