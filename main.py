"""
Lore - CLI
Terminal interface for Lore, using the shared assistant core and persistent sessions.
"""

from src.assistant import ask_ai
from src.db.database import init_db
from src.db.conversations import create_session, save_message, list_sessions, get_session_messages


def print_sessions():
    sessions = list_sessions()
    if not sessions:
        print("No saved conversations yet.\n")
        return
    for s in sessions:
        title = s["title"] or "(untitled)"
        print(f"  {s['id'][:8]}  {s['started_at'][:19]}  {title}")
    print()


def main():
    init_db()

    print("================================")
    print("Lore")
    print("================================")
    print("Commands: 'sessions' to list past conversations, 'load <id>' to resume one, 'exit' to quit.")


    session_id = None  
    conversation_history = []

    while True:
        question = input("You: ")

        if not question.strip():
            continue

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if question.lower() == "sessions":
            print_sessions()
            continue

        if question.lower().startswith("load "):
            short_id = question.split(" ", 1)[1].strip()
            matches = [s for s in list_sessions() if s["id"].startswith(short_id)]
            if not matches:
                print("No matching session found.\n")
                continue
            session_id = matches[0]["id"]
            past_messages = get_session_messages(session_id)
            conversation_history = [
                {"role": m["role"], "content": m["content"]} for m in past_messages
            ]
            print(f"Resumed conversation: {matches[0]['title']}\n")
            continue

        if session_id is None:
            session_id = create_session()

        answer, sources, tool = ask_ai(question, conversation_history)

        save_message(session_id, "user", question)
        save_message(session_id, "assistant", answer)

        print(f"[Tool: {tool}]")
        print(f"\nLore: {answer}")
        print(f"(sources: {', '.join(sources)})\n")

if __name__ == "__main__":
    main()