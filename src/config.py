"""
Lore - Configuration
Single source of truth for all configurable values, loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# AI models
CHAT_MODEL = os.getenv("MODEL_NAME", "llama3")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
ROUTER_MODEL = os.getenv("ROUTER_MODEL", CHAT_MODEL)

# Storage paths
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
DB_PATH = os.getenv("DB_PATH", "lore.db")
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "knowledge")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "lore_knowledge")

# External APIs (optional)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Conversation behavior
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))