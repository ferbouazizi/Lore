# Lore

A lightweight local AI assistant for exploring fictional worlds, characters, and stories.

Lore runs entirely on your machine using open-source tools. It retrieves relevant information from a local knowledge base before answering, and automatically decides whether a question needs local knowledge, live movie data, or neither - so answers are grounded in real content instead of guesswork.

No cloud dependency required for core functionality. No mandatory external API. Your conversations and knowledge base stay on your machine.

---

## Features

* Two interfaces: a terminal CLI and a local Streamlit web UI
* Local AI inference with Ollama (chat + embeddings)
* Retrieval-Augmented Generation (RAG) - answers grounded in a local knowledge base, with sources shown per response
* Automatic tool routing - Lore decides per question whether to search the knowledge base, query TMDB, or answer directly
* Knowledge base supports `.txt`, `.md`, and `.pdf` files, with incremental indexing (only new or edited files are re-embedded)
* Persistent conversation history (SQLite) - list, resume, or start fresh sessions, in both the CLI and the UI
* Consistent assistant persona via a system prompt
* Automated test suite (pytest)
* Centralized configuration via environment variables
* Private and offline-first for all core functionality

---

## How It Works

```
User Question
     |
     v
Router decides: knowledge search / movie search / direct answer
     |
     v
(if needed) Embed Question -> ChromaDB Similarity Search -> Relevant Content
     |
     v
Prompt Built (context + conversation history + question)
     |
     v
Ollama Local Server (chat model)
     |
     v
Grounded Response + Sources
     |
     v
Saved to SQLite (session + message history)
```

---

## Tech Stack

| Technology       | Purpose                                    |
| ---------------- | ------------------------------------------- |
| Python           | Core application                            |
| Ollama           | Local AI runtime (chat + embeddings)        |
| Llama 3          | Language model (chat + routing)             |
| nomic-embed-text | Embedding model for semantic search         |
| ChromaDB         | Local vector database                       |
| SQLite           | Local conversation storage                  |
| Streamlit        | Local web UI                                |
| pypdf            | PDF text extraction for the knowledge base  |
| TMDB API         | Optional live movie data                    |
| pytest           | Automated testing                           |

---

## Installation

### Requirements

* Python 3.10+
* Ollama

Install Ollama: https://ollama.com

Download the required models:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### Clone & Set Up

```bash
git clone <repository-url>
cd Lore
python -m venv venv
```

Windows:
```powershell
venv\Scripts\activate
```
macOS/Linux:
```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### Configure (optional)

Copy `.env.example` to `.env`. All values have sensible defaults - only `TMDB_API_KEY` is worth setting, and only if you want movie-search questions to return live data:

```
TMDB_API_KEY=
MODEL_NAME=llama3
```

Get a free TMDB key at https://www.themoviedb.org/ (Settings -> API). Everything else works fully offline without it.

### Build the Knowledge Base Index

Run once, and again any time you add or edit files under `knowledge/`:

```bash
python -m src.rag.embeddings
```

---

## Usage

**Terminal:**
```bash
python main.py
```

**Web UI:**
```bash
streamlit run app.py
```

**Windows shortcut** (`run.bat`):
```bat
run.bat        :: terminal
run.bat ui     :: web UI
```

Example session:
```
Lore
You: Who is Gwen Stacy?

Lore: Gwen Stacy, also known as Spider-Woman or Ghost-Spider, is a Spider-Person
from Earth-65...
(sources: knowledge/characters/gwen_stacy.txt, knowledge/marvel/spiderman.txt)

You: find Spider-Man movies rated above 8
[Tool: search_movies]
Lore: Here are Spider-Man movies rated above 8...

You: sessions
  a1b2c3d4  2026-08-03T14:22:10  Who is Gwen Stacy?

You: load a1b2c3d4
Resumed conversation: Who is Gwen Stacy?
```

Movie questions, knowledge questions, and small talk are all routed automatically - there's no manual command syntax to remember.

---

## Adding Knowledge

Drop `.txt`, `.md`, or `.pdf` files into any subfolder under `knowledge/`, then rebuild the index:

```bash
python -m src.rag.embeddings
```

Indexing is incremental: unchanged files are skipped, edited files replace their old entry, and identical content under a different filename is treated as a duplicate and skipped.

---

## Running Tests

```bash
pytest
```

Runs unit tests (knowledge loader, prompt construction) and an integration test suite (retriever - requires Ollama running and the index already built).

---

## Project Structure

```
Lore/
│
├── main.py                  CLI entry point
├── app.py                   Streamlit UI entry point
├── run.bat                  Windows launcher (CLI or UI)
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── .streamlit/
│    └── config.toml         Dark theme for native Streamlit UI elements
│
├── src/
│    ├── config.py           Centralized settings, loaded from environment variables
│    ├── assistant.py        Shared core: builds prompts, calls the chat model
│    ├── agent/
│    │    ├── router.py      Decides which tool (if any) a question needs
│    │    └── tools.py       Tool registry: knowledge search, movie search
│    ├── rag/
│    │    ├── embeddings.py  Embedding generation + incremental ChromaDB indexing
│    │    ├── retriever.py   Similarity search over the knowledge base
│    │    └── prompt.py      Pure prompt-construction logic (unit tested)
│    ├── movies/
│    │    └── api.py         TMDB search with optional rating filtering
│    ├── db/
│    │    ├── database.py    SQLite schema + connection
│    │    └── conversations.py  Session/message persistence
│    └── utils/
│         ├── loader.py             Walks knowledge/ and loads supported files
│         └── document_processor.py Per-format text extraction (.txt/.md/.pdf)
│
├── knowledge/
│    ├── marvel/
│    ├── movies/
│    └── characters/
│
└── tests/
     ├── test_loader.py
     ├── test_prompt.py
     └── test_retriever.py
```

---

## Development Philosophy

Lore focuses on:

* Understanding AI systems from the fundamentals, not through a heavy framework
* Keeping the architecture lightweight - complexity is added only when it's earned
* Prioritizing privacy and local execution
* One source of truth per concern: config in `config.py`, RAG logic in `assistant.py`, tool decisions in `router.py`

---

## Roadmap

V1 is complete:

* [x] Local AI chat (CLI + Streamlit UI)
* [x] RAG with semantic search (ChromaDB + embeddings)
* [x] Multi-format knowledge base with incremental indexing
* [x] Persistent, resumable conversation sessions
* [x] Automatic tool routing (knowledge search / movie search / direct answer)
* [x] Automated test suite
* [x] Centralized configuration

**Possible next steps:** web deployment, voice interface, Docker packaging, a desktop-app wrapper.

---

## License

This project is for learning, experimentation, and personal development.
