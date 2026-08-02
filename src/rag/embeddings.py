"""
Lore - Embeddings & Vector Store
Converts knowledge documents into embeddings and stores them in ChromaDB.
Incremental: only new documents are embedded; duplicates are skipped.
"""

import hashlib

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


def hash_content(text):
    """Return a short, stable fingerprint of a piece of text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(COLLECTION_NAME)


def document_already_indexed(collection, content_hash):
    """Check whether a document with this exact content hash is already stored."""
    existing = collection.get(where={"hash": content_hash})
    return len(existing["ids"]) > 0


def build_vector_store():
    """
    Load all knowledge documents and add any that aren't already indexed.
    Safe to run repeatedly - already-indexed documents are skipped.
    """
    collection = get_collection()
    documents = load_knowledge_base()

    added = 0
    skipped = 0

    for doc in documents:
        content_hash = hash_content(doc["content"])

        if document_already_indexed(collection, content_hash):
            skipped += 1
            continue

        embedding = get_embedding(doc["content"])
        collection.add(
            ids=[content_hash],
            embeddings=[embedding],
            documents=[doc["content"]],
            metadatas=[{"source": doc["source"], "hash": content_hash}]
        )
        added += 1

    print(f"Indexed {added} new document(s), skipped {skipped} already-indexed document(s).")


if __name__ == "__main__":
    build_vector_store()