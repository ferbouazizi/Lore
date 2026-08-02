"""
Lore - Phase 4
A local AI assistant that answers using retrieved knowledge (RAG).
"""

import ollama

from src.rag.retriever import get_relevant_documents

CHAT_MODEL = "llama3"


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


def ask_ai(question):
    """Retrieve relevant knowledge, build a grounded prompt, and get the AI's answer."""
    retrieved_docs = get_relevant_documents(question)
    prompt = build_prompt(question, retrieved_docs)

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    sources = [doc["source"] for doc in retrieved_docs]
    return response["message"]["content"], sources


def main():
    print("================================")
    print("Lore")
    print("================================")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer, sources = ask_ai(question)
        print(f"\nAI: {answer}")
        print(f"(sources: {', '.join(sources)})\n")


if __name__ == "__main__":
    main()