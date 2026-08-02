"""
Lore - Streamlit UI
Local browser-based chat interface, styled as a calm, premium dark-blue AI research terminal.
"""

from datetime import datetime

import streamlit as st

try:
    import ollama
except ImportError:
    ollama = None

from src.assistant import ask_ai, CHAT_MODEL


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="LORE — Local AI Assistant", page_icon=None, layout="wide")


# ---------------------------------------------------------------------------
# Design tokens + global styling
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --bg: #050914;
        --grad-1: #07152F;
        --grad-2: #0B1E3D;
        --panel: #0D172A;
        --panel-2: #111C32;
        --panel-3: #152542;
        --text: #F5F7FA;
        --muted: #8B95A7;
        --accent: #6FA8FF;
        --glow: #3B82F6;
        --highlight: #6D5DFB;
    }

    /* ---- base ---- */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }

    .stApp {
        background:
            radial-gradient(circle at 15% -10%, rgba(59, 130, 246, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 85% 10%, rgba(109, 93, 251, 0.10) 0%, transparent 40%),
            linear-gradient(180deg, var(--grad-2) 0%, var(--grad-1) 35%, var(--bg) 100%);
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 2.4rem;
        max-width: 880px;
    }

    /* ---- sidebar ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--panel-2) 0%, var(--bg) 100%);
        border-right: 1px solid rgba(111, 168, 255, 0.12);
    }

    .lore-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.9rem;
        letter-spacing: 0.02em;
        color: var(--text);
        margin-bottom: 0;
        line-height: 1.1;
    }

    .lore-tagline {
        font-family: 'Space Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        margin-top: 4px;
        margin-bottom: 14px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-family: 'Space Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.1em;
        color: var(--accent);
        background: rgba(111, 168, 255, 0.08);
        border: 1px solid rgba(111, 168, 255, 0.18);
        border-radius: 20px;
        padding: 5px 12px;
        margin-bottom: 1.6rem;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--glow);
        box-shadow: 0 0 8px var(--glow), 0 0 14px rgba(59, 130, 246, 0.5);
        flex-shrink: 0;
    }

    .status-dot.offline {
        background: var(--muted);
        box-shadow: none;
    }

    .sidebar-section-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.64rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--muted);
        border-top: 1px solid rgba(245, 247, 250, 0.08);
        padding-top: 1.1rem;
        margin-top: 1.2rem;
        margin-bottom: 0.7rem;
    }

    .feature-item {
        font-family: 'Inter', sans-serif;
        font-size: 0.87rem;
        font-weight: 400;
        color: var(--text);
        padding: 4px 0;
        opacity: 0.92;
    }

    .feature-item span.marker {
        color: var(--accent);
        margin-right: 8px;
        font-family: 'Space Mono', monospace;
    }

    .kb-item {
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.04em;
        color: var(--muted);
        padding: 5px 10px;
        margin-bottom: 5px;
        background: rgba(21, 37, 66, 0.55);
        border: 1px solid rgba(111, 168, 255, 0.10);
        border-radius: 6px;
    }

    .sys-row {
        display: flex;
        justify-content: space-between;
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        padding: 4px 0;
        color: var(--muted);
    }

    .sys-row span.val {
        color: var(--text);
    }

    /* ---- main header ---- */
    .hero {
        margin-bottom: 2rem;
    }

    .hero-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.6rem;
        color: var(--text);
        letter-spacing: -0.01em;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.02rem;
        color: var(--muted);
        margin-bottom: 2px;
    }

    .hero-caption {
        font-family: 'Space Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
        color: var(--accent);
        opacity: 0.75;
        margin-top: 10px;
    }

    /* ---- chat: user message ---- */
    .user-bubble-wrap {
        display: flex;
        justify-content: flex-end;
        margin: 20px 0 8px 0;
    }

    .user-bubble {
        background: linear-gradient(135deg, #152D55 0%, #1D4ED8 130%);
        border-radius: 16px 16px 4px 16px;
        padding: 13px 19px;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.55;
        box-shadow: 0 6px 20px rgba(29, 78, 216, 0.25);
    }

    /* ---- chat: AI glass card ---- */
    .ai-card {
        position: relative;
        background: rgba(13, 23, 42, 0.75);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(111, 168, 255, 0.2);
        border-radius: 16px;
        padding: 20px 24px 18px 24px;
        margin: 6px 0 20px 0;
        max-width: 84%;
        box-shadow: 0 0 24px rgba(59, 130, 246, 0.08), 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .ai-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Space Mono', monospace;
        font-size: 0.66rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 12px;
    }

    .ai-header .tag {
        color: var(--accent);
        font-weight: 700;
    }

    .ai-body {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 0.97rem;
        line-height: 1.68;
        color: var(--text);
    }

    .source-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 15px;
    }

    .source-pill {
        font-family: 'Space Mono', monospace;
        font-size: 0.66rem;
        color: var(--accent);
        background: rgba(111, 168, 255, 0.08);
        border: 1px solid rgba(111, 168, 255, 0.22);
        border-radius: 20px;
        padding: 4px 12px;
        letter-spacing: 0.02em;
    }

    .source-pill::before {
        content: "SRC: ";
        color: var(--muted);
    }

    /* ---- chat input ---- */
    [data-testid="stChatInput"] {
        background: var(--panel-2);
        border: 1px solid rgba(111, 168, 255, 0.18);
        border-radius: 14px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(111, 168, 255, 0.55);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15), 0 4px 18px rgba(0, 0, 0, 0.3);
    }

    [data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif;
        color: var(--text) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_model_status():
    """Return True if Ollama is reachable, False otherwise."""
    if ollama is None:
        return False
    try:
        ollama.list()
        return True
    except Exception:
        return False


def render_user_message(text):
    st.markdown(
        f"""
        <div class="user-bubble-wrap">
            <div class="user-bubble">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_message(text, sources, timestamp):
    source_html = ""
    if sources:
        pills = "".join(f'<div class="source-pill">{s}</div>' for s in sources)
        source_html = f'<div class="source-row">{pills}</div>'

    st.markdown(
        f"""
        <div class="ai-card">
            <div class="ai-header">
                <span><span class="tag">LORE RESPONSE</span> · {timestamp}</span>
                <span>{CHAT_MODEL.upper()}</span>
            </div>
            <div class="ai-body">{text}</div>
            {source_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<div class="lore-title">LORE</div>', unsafe_allow_html=True)
    st.markdown('<div class="lore-tagline">Local AI Knowledge Assistant</div>', unsafe_allow_html=True)

    is_online = check_model_status()
    dot_class = "" if is_online else "offline"
    status_text = "SYSTEM ONLINE" if is_online else "SYSTEM OFFLINE"
    st.markdown(
        f'<div class="status-pill"><span class="status-dot {dot_class}"></span>{status_text}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section-label">Capabilities</div>', unsafe_allow_html=True)
    features = [
        "Retrieval Augmented Generation",
        "Conversation Memory",
        "Local LLM",
        "Movie Search",
    ]
    for f in features:
        st.markdown(
            f'<div class="feature-item"><span class="marker">▸</span>{f}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-section-label">Knowledge Base</div>', unsafe_allow_html=True)
    kb_items = ["MARVEL DATABASE", "CHARACTERS", "MOVIES"]
    for item in kb_items:
        st.markdown(f'<div class="kb-item">{item}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">System</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sys-row"><span>Model</span><span class="val">Llama</span></div>
        <div class="sys-row"><span>Engine</span><span class="val">Ollama</span></div>
        <div class="sys-row"><span>Mode</span><span class="val">Local</span></div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main hero
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">LORE</div>
        <div class="hero-subtitle">Your personal AI knowledge companion</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []


# ---------------------------------------------------------------------------
# Render existing conversation
# ---------------------------------------------------------------------------

for msg in st.session_state.display_messages:
    if msg["role"] == "user":
        render_user_message(msg["content"])
    else:
        render_ai_message(msg["content"], msg.get("sources", []), msg.get("timestamp", ""))


# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------

question = st.chat_input("Ask Lore anything...")

if question:
    render_user_message(question)
    st.session_state.display_messages.append({"role": "user", "content": question})

    with st.spinner("Searching archive..."):
        answer, sources = ask_ai(question, st.session_state.conversation_history)

    timestamp = datetime.now().strftime("%H:%M:%S")
    render_ai_message(answer, sources, timestamp)

    st.session_state.display_messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "timestamp": timestamp,
    })