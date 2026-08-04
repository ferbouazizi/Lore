"""
Lore - Embeddings & Vector Store
Converts knowledge documents into embeddings and stores them in ChromaDB.
Incremental: only new documents are embedded; duplicates are skipped.
"""

import hashlib

import ollama
import chromadb

from src.utils.loader import load_knowledge_base

from src.config import EMBEDDING_MODEL, CHROMA_PATH, COLLECTION_NAME


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
    Load all knowledge documents and keep the vector store in sync:
    - New documents are embedded and added
    - Edited documents (same source, different content) replace their old entry
    - Unchanged documents are skipped
    - Identical content under a different filename is skipped (true duplicate)
    """
    collection = get_collection()
    documents = load_knowledge_base()

    added = 0
    updated = 0
    skipped = 0

    for doc in documents:
        content_hash = hash_content(doc["content"])

        existing_for_source = collection.get(where={"source": doc["source"]})

        if existing_for_source["ids"]:
            existing_hash = existing_for_source["metadatas"][0]["hash"]

            if existing_hash == content_hash:
                skipped += 1
                continue

            # File was edited since last indexing - remove the old entry, add the new one
            collection.delete(ids=existing_for_source["ids"])
            embedding = get_embedding(doc["content"])
            collection.add(
                ids=[content_hash],
                embeddings=[embedding],
                documents=[doc["content"]],
                metadatas=[{"source": doc["source"], "hash": content_hash}]
            )
            updated += 1
            continue

        if document_already_indexed(collection, content_hash):
            # Identical content already stored under a different filename
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

    print(f"Indexed {added} new, updated {updated} edited, skipped {skipped} unchanged.")

if __name__ == "__main__":
    build_vector_store()