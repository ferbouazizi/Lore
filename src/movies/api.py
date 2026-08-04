import requests

from src.config import TMDB_API_KEY

TMDB_BASE_URL = "https://api.themoviedb.org/3"


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