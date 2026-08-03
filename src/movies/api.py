import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """Search TMDB for a movie by title and return its key details, or None if not found."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": title}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data["results"]:
        return None

    movie = data["results"][0]
    return {
        "title": movie["title"],
        "release_date": movie.get("release_date", "Unknown"),
        "rating": movie.get("vote_average", "N/A"),
        "overview": movie.get("overview", "No overview available.")
    }
def search_movies(keyword, min_rating=None, limit=5):
    """Search TMDB for movies matching a keyword, optionally filtered by minimum rating."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": keyword}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for movie in data["results"]:
        rating = movie.get("vote_average", 0)
        if min_rating is not None and rating < min_rating:
            continue
        results.append({
            "title": movie["title"],
            "release_date": movie.get("release_date", "Unknown"),
            "rating": rating
        })

    return results[:limit]