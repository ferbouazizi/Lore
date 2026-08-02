"""Tests for prompt construction logic."""

from src.rag.prompt import build_prompt


def test_prompt_includes_the_question():
    docs = [{"content": "Some knowledge content.", "source": "test.txt"}]
    prompt = build_prompt("Who is Gwen Stacy?", docs)
    assert "Who is Gwen Stacy?" in prompt


def test_prompt_includes_all_retrieved_content():
    docs = [
        {"content": "First document content.", "source": "a.txt"},
        {"content": "Second document content.", "source": "b.txt"},
    ]
    prompt = build_prompt("A question", docs)
    assert "First document content." in prompt
    assert "Second document content." in prompt


def test_prompt_handles_empty_retrieval():
    """Even with no retrieved documents, prompt building shouldn't crash."""
    prompt = build_prompt("A question with no matches", [])
    assert "A question with no matches" in prompt