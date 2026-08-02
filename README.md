# Lore

A lightweight local AI assistant for exploring fictional worlds, characters, and stories.

Lore runs AI models locally using open-source tools, providing a private assistant experience directly from the terminal.

No cloud dependency. No external API required. Your conversations stay on your machine.

---

## Features

* Terminal-based AI chat interface
* Local AI inference with Ollama
* Private and offline-first workflow
* Simple Python architecture
* Designed to grow into a knowledge-aware assistant

---

## How It Works

Lore connects a Python application with a locally running language model.

```
User Input
    |
    v
Lore CLI
    |
    v
Ollama Local Server
    |
    v
AI Model
    |
    v
Response
```

---

## Tech Stack

| Technology | Purpose          |
| ---------- | ---------------- |
| Python     | Core application |
| Ollama     | Local AI runtime |
| Llama 3    | Language model   |

---

## Installation

### Requirements

* Python 3.10+
* Ollama

Install Ollama:

https://ollama.com

Download a model:

```bash
ollama pull llama3
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

## Usage

Start Lore:

```bash
python main.py
```

Example:

```
Lore

You: Who is Spider-Man?

AI: Spider-Man is a Marvel superhero...
```

Exit the program:

```
exit
```

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
│
├── knowledge/
│
└── tests/
```

---

## Current Status

Lore is currently in its first development phase.

The current version focuses on:

* Building a local AI interface
* Connecting Python applications with local language models
* Creating a clean foundation for future improvements

---

## Development Philosophy

Lore focuses on:

* Understanding AI systems from the fundamentals
* Keeping the architecture lightweight
* Prioritizing privacy and local execution
* Adding complexity only when necessary

---

## License

This project is for learning, experimentation, and personal development.
