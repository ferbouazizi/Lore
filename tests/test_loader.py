"""Tests for the knowledge base loader."""

from src.utils.loader import load_knowledge_base


def test_load_knowledge_base_returns_documents():
    """The loader should find at least one document."""
    documents = load_knowledge_base()
    assert len(documents) > 0


def test_documents_have_required_fields():
    """Every loaded document must have a source and non-empty content."""
    documents = load_knowledge_base()
    for doc in documents:
        assert "source" in doc
        assert "content" in doc
        assert len(doc["content"]) > 0


def test_documents_are_text_files():
    """Every loaded document's source should be a .txt file."""
    documents = load_knowledge_base()
    for doc in documents:
        assert doc["source"].endswith(".txt")