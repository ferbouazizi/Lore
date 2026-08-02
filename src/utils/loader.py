"""
Lore - Knowledge Base Loader
Reads all .txt files from the knowledge/ folder into memory.
"""

from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge")


def load_knowledge_base():
    """
    Read every .txt file under knowledge/ (including subfolders).
    Returns a list of dicts: {"source": <file path>, "content": <file text>}
    """
    documents = []

    for file_path in KNOWLEDGE_DIR.rglob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "source": str(file_path),
            "content": text.strip()
        })

    return documents


if __name__ == "__main__":
    docs = load_knowledge_base()
    print(f"Loaded {len(docs)} documents.\n")
    for doc in docs:
        preview = doc["content"][:80].replace("\n", " ")
        print(f"- {doc['source']}: {preview}...")