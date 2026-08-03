"""
Lore - Agent Tools
Defines the capabilities the router can choose between.
"""

from src.rag.retriever import get_relevant_documents
from src.movies.api import search_movies


def run_search_knowledge(args):
    """Search the local knowledge base and return matching content as context text."""
    query = args.get("query", "")
    docs = get_relevant_documents(query)
    context = "\n\n".join(doc["content"] for doc in docs)
    sources = [doc["source"] for doc in docs]
    return context, sources


def run_search_movies(args):
    """Search TMDB, optionally filtered by minimum rating."""
    keyword = args.get("keyword", "")
    min_rating = args.get("min_rating")

    movies = search_movies(keyword, min_rating=min_rating)

    if not movies:
        return "No matching movies found.", []

    lines = [f"{m['title']} ({m['release_date'][:4]}) - Rating: {m['rating']}/10" for m in movies]
    context = "\n".join(lines)
    return context, []


TOOLS = {
    "search_knowledge": {
        "description": "Search the local knowledge base for facts about characters, movies, and fictional universes.",
        "run": run_search_knowledge
    },
    "search_movies": {
        "description": "Search for live movie data from TMDB, optionally filtered by a minimum rating (e.g. 'movies rated above 8').",
        "run": run_search_movies
    }
}