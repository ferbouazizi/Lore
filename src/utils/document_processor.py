"""
Lore - Document Processor
Extracts plain text from different file formats.
"""

from pathlib import Path
from pypdf import PdfReader


def read_txt(path):
    return path.read_text(encoding="utf-8").strip()


def read_markdown(path):
    # Markdown is plain text underneath - no special parsing needed for embeddings
    return path.read_text(encoding="utf-8").strip()


def read_pdf(path):
    reader = PdfReader(path)
    pages_text = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages_text).strip()


EXTENSION_HANDLERS = {
    ".txt": read_txt,
    ".md": read_markdown,
    ".pdf": read_pdf,
}


def load_document(path):
    """Read a single file and return its plain text, using the right handler for its extension."""
    handler = EXTENSION_HANDLERS.get(path.suffix.lower())
    if handler is None:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    return handler(path)