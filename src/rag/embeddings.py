"""
Lore - Embeddings & Vector Store
Converts knowledge documents into embeddings and stores them in ChromaDB.
"""

import ollama
import chromadb

from src.utils.loader import load_knowledge_base

EMBEDDING_MODEL = "nomic-embed-text"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "lore_knowledge"


def get_embedding(text):
    """Convert a piece of text into an embedding vector using Ollama."""
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
    return response["embedding"]


def build_vector_store():
    """
    Load all knowledge documents, embed each one, and store them in ChromaDB.
    Safe to re-run: it rebuilds the collection from scratch each time.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Start fresh each time so the store always matches knowledge/
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(COLLECTION_NAME)

    documents = load_knowledge_base()

    for i, doc in enumerate(documents):
        embedding = get_embedding(doc["content"])
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[doc["content"]],
            metadatas=[{"source": doc["source"]}]
        )

    print(f"Stored {len(documents)} documents in ChromaDB.")


if __name__ == "__main__":
    build_vector_store()