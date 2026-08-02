"""
Lore - Streamlit UI
Local browser-based chat interface, using the shared assistant core.
"""

import streamlit as st

from src.assistant import ask_ai

st.set_page_config(page_title="Lore", page_icon="🕮")
st.title("🕮 Lore")
st.caption("A local AI assistant for exploring fictional worlds, characters, and stories.")

# Initialize conversation history once per browser session
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

# Render past messages
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            st.caption(f"Sources: {', '.join(msg['sources'])}")

# Handle new input
question = st.chat_input("Ask Lore something...")

if question:
    with st.chat_message("user"):
        st.write(question)
    st.session_state.display_messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask_ai(question, st.session_state.conversation_history)
        st.write(answer)
        if sources:
            st.caption(f"Sources: {', '.join(sources)}")

    st.session_state.display_messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })