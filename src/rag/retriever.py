"""
Lore - Retriever
Given a question, finds the most relevant stored documents.
"""

import chromadb

from src.rag.embeddings import get_embedding, CHROMA_PATH, COLLECTION_NAME


def get_relevant_documents(question, n_results=3):
    """
    Embed the question and return the most similar stored documents.
    Returns a list of dicts: {"source": ..., "content": ...}
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    matches = []
    for content, metadata in zip(results["documents"][0], results["metadatas"][0]):
        matches.append({"source": metadata["source"], "content": content})

    return matches


if __name__ == "__main__":
    test_question = "Who is ned leeds?"
    matches = get_relevant_documents(test_question)

    print(f"Question: {test_question}\n")
    for match in matches:
        preview = match["content"][:80].replace("\n", " ")
        print(f"- {match['source']}: {preview}...")