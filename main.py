
"""
Lore - Phase 1
A simple command-line AI assistant that communicates with a local AI model via Ollama.
"""

import ollama


def ask_ai(question):
    """Send a question to the local AI model and return its response."""
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return response["message"]["content"]


def main():
    print("================================")
    print("Lore")
    print("Your Fictional Universe Assistant")
    print("================================")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = ask_ai(question)
        print(f"\nAI: {answer}\n")


if __name__ == "__main__":
    main()
