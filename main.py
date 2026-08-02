import ollama

from src.rag.retriever import get_relevant_documents
from src.movies.api import search_movie
from src.rag.prompt import build_prompt


CHAT_MODEL = "llama3"

SYSTEM_PROMPT = """You are Lore, a local AI assistant that helps users explore fictional worlds, characters, and stories.
Answer using the provided context when available. If the context doesn't cover the question, say so honestly rather than guessing.
Keep answers clear, concise, and conversational."""


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

    # Save conversation memory
    conversation_history.append(
        {"role": "user", "content": question}
    )

    conversation_history.append(
        {"role": "assistant", "content": answer}
    )

    # Keep last 10 exchanges
    conversation_history[:] = conversation_history[-20:]

    sources = [doc["source"] for doc in retrieved_docs]

    return answer, sources


def main():
    print("================================")
    print("Lore")
    print("================================")
    print("Local AI Assistant with RAG + Movie Search")
    print("Type 'exit' to quit.")
    print("Use 'movie: title' to search movies.\n")

    conversation_history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Movie API command
        if question.lower().startswith("movie:"):
            title = question.split(":", 1)[1].strip()

            movie = search_movie(title)

            if movie:
                print(f"\n🎬 {movie['title']} ({movie['release_date']})")
                print(f"⭐ Rating: {movie['rating']}/10")
                print(f"\n{movie['overview']}\n")
            else:
                print("\nNo movie found with that title.\n")

            continue

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