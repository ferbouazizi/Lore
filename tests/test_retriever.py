"""
Integration tests for the retriever.
Requires Ollama running and the ChromaDB store already built
(run `python -m src.rag.embeddings` first).
"""

from src.rag.retriever import get_relevant_documents


def test_retriever_returns_results():
    results = get_relevant_documents("Who is Gwen Stacy?")
    assert len(results) > 0


def test_retriever_finds_relevant_source():
    """A clearly-targeted question should surface the matching file."""
    results = get_relevant_documents("Who is Gwen Stacy?")
    sources = [doc["source"] for doc in results]
    assert any("gwen_stacy" in source.lower() for source in sources)