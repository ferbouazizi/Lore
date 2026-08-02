"""
Lore - Knowledge Base Loader
Reads all supported knowledge files (.txt, .md, .pdf) into memory.
"""

from pathlib import Path

from src.utils.document_processor import load_document, EXTENSION_HANDLERS

KNOWLEDGE_DIR = Path("knowledge")


def load_knowledge_base():
    """
    Read every supported file under knowledge/ (including subfolders).
    Returns a list of dicts: {"source": <file path>, "content": <file text>}
    """
    documents = []

    for extension in EXTENSION_HANDLERS:
        for file_path in KNOWLEDGE_DIR.rglob(f"*{extension}"):
            content = load_document(file_path)
            if content:
                documents.append({
                    "source": str(file_path),
                    "content": content
                })

    return documents