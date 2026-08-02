# Lore

A lightweight local AI assistant for exploring fictional worlds, characters, and stories.

Lore runs AI models locally using open-source tools, providing a private, knowledge-grounded assistant experience directly from the terminal. It retrieves relevant information from a local knowledge base before answering, so responses are grounded in real, curated content rather than the model's memory alone.

No cloud dependency required for core functionality. No mandatory external API. Your conversations stay on your machine.

---

## Features

* Terminal-based AI chat interface
* Local AI inference with Ollama
* Retrieval-Augmented Generation (RAG) — answers grounded in a real knowledge base, with sources shown for every response
* Semantic search over the knowledge base via embeddings and ChromaDB
* Conversation memory within a session
* Consistent assistant persona via a system prompt
* Optional live movie data lookup via TMDB
* Automated test suite (pytest)
* Private and offline-first workflow for all core features
* Simple, modular Python architecture

---

## How It Works

Lore combines a locally running language model with a local knowledge base, retrieving relevant information before generating a response.

```
User Question
     |
     v
Embed Question (Ollama - nomic-embed-text)
     |
     v
ChromaDB Similarity Search
     |
     v
Relevant Knowledge Retrieved
     |
     v
Prompt Built (context + conversation history + question)
     |
     v
Ollama Local Server (Llama 3)
     |
     v
Grounded Response + Sources
```

---

## Tech Stack

| Technology         | Purpose                              |
| ------------------ | ------------------------------------- |
| Python              | Core application                      |
| Ollama              | Local AI runtime (chat + embeddings)  |
| Llama 3             | Language model                        |
| nomic-embed-text    | Embedding model for semantic search   |
| ChromaDB            | Local vector database                 |
| TMDB API            | Optional live movie data              |
| pytest              | Automated testing                     |

---

## Installation

### Requirements

* Python 3.10+
* Ollama

Install Ollama:
https://ollama.com

Download the required models:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

---

### Clone Repository

```bash
git clone <repository-url>
cd Lore
```

---

### Create Virtual Environment

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment (optional — only needed for TMDB)

Copy `.env.example` to `.env` and add your TMDB API key:
```
TMDB_API_KEY=your_key_here
MODEL_NAME=llama3
```

Get a free key at https://www.themoviedb.org/ (Settings → API). Lore works fully without this — it's only needed for the `movie:` command.

---

### Build the Knowledge Base Index

Run this once (and again any time you add or change files in `knowledge/`):

```bash
python -m src.rag.embeddings
```

---

## Usage

Start Lore:
```bash
python main.py
```

Example:
```
Lore
You: Who is Gwen Stacy?

AI: Gwen Stacy, also known as Spider-Woman or Ghost-Spider, is a Spider-Person
from Earth-65...
(sources: knowledge/characters/gwen_stacy.txt, knowledge/marvel/spiderman.txt)

You: What about her allies?

AI: [remembers the previous question and answers accordingly]

You: movie: Spider-Man: Into the Spider-Verse
🎬 Spider-Man: Into the Spider-Verse (2018-12-06)
Rating: 8.4/10
An animated film exploring the multiverse...
```

Exit the program:
```
exit
```

---

## Running Tests

```bash
pytest
```

Runs unit tests (knowledge loader, prompt construction) and integration tests (retrieval — requires Ollama running and the index already built).

---

## Project Structure

```
Lore/
│
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── src/
│   ├── ai/
│   ├── rag/
│   │    ├── embeddings.py
│   │    ├── retriever.py
│   │    └── prompt.py
│   ├── movies/
│   │    └── api.py
│   └── utils/
│        └── loader.py
│
├── knowledge/
│   ├── marvel/
│   ├── movies/
│   └── characters/
│
└── tests/
     ├── test_loader.py
     ├── test_prompt.py
     └── test_retriever.py
```

---

## Current Status

Lore has completed its full V1 roadmap:

* [x] Local AI chat interface (Ollama)
* [x] Movie/character knowledge base
* [x] Semantic search via embeddings + ChromaDB
* [x] Full RAG pipeline (retrieval-grounded answers with sources)
* [x] Conversation memory
* [x] Assistant persona via system prompt
* [x] Optional live movie data (TMDB)
* [x] Automated test suite

---

## Development Philosophy

Lore focuses on:

* Understanding AI systems from the fundamentals
* Keeping the architecture lightweight — no heavier frameworks than necessary
* Prioritizing privacy and local execution
* Adding complexity only when it's earned, not by default

---

## Future Improvements

* Web interface (React frontend + FastAPI backend)
* Voice assistant support
* Improved retrieval (reranking, relevance thresholds)
* Docker support and cloud deployment option

---

## License

This project is for learning, experimentation, and personal development.
