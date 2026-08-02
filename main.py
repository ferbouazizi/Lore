"""
Lore - CLI
Terminal interface for Lore, using the shared assistant core.
"""

from src.assistant import ask_ai


def main():
    print("================================")
    print("Lore")
    print("================================")
    print("Type 'exit' to quit.\n")

    conversation_history = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if question.lower().startswith("movie:"):
            from src.movies.api import search_movie
            title = question.split(":", 1)[1].strip()
            movie = search_movie(title)
            if movie:
                print(f"\n🎬 {movie['title']} ({movie['release_date']})")
                print(f"Rating: {movie['rating']}/10")
                print(f"{movie['overview']}\n")
            else:
                print("\nNo movie found with that title.\n")
            continue

        answer, sources = ask_ai(question, conversation_history)
        print(f"\nAI: {answer}")
        print(f"(sources: {', '.join(sources)})\n")


if __name__ == "__main__":
    main()