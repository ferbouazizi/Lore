"""
Lore - Conversation Storage
Save, list, and load conversation sessions.
"""

import uuid
from datetime import datetime

from src.db.database import get_connection


def create_session():
    """Start a new conversation session and return its ID."""
    session_id = str(uuid.uuid4())
    started_at = datetime.now().isoformat()

    conn = get_connection()
    conn.execute(
        "INSERT INTO sessions (id, started_at) VALUES (?, ?)",
        (session_id, started_at)
    )
    conn.commit()
    conn.close()

    return session_id


def save_message(session_id, role, content):
    """Save one message to a session, and set the session title if it doesn't have one yet."""
    timestamp = datetime.now().isoformat()

    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (session_id, role, content, timestamp)
    )

    if role == "user":
        cursor = conn.execute("SELECT title FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        if row and row["title"] is None:
            title = content[:60]
            conn.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))

    conn.commit()
    conn.close()


def get_session_messages(session_id):
    """Return all messages for a session, oldest first."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return messages


def list_sessions():
    """Return all sessions, most recent first."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT id, title, started_at FROM sessions ORDER BY started_at DESC"
    )
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sessions