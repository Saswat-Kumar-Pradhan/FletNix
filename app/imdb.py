import requests

def fetch_imdb_reviews(title: str):
    """
    Fetch movie reviews and ratings using OMDB API (as IMDB proxy)
    Get your free key from: https://www.omdbapi.com/apikey.aspx
    """
    API_KEY = "c581aa41"
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        return {"rating": None, "reviews": []}

    data = res.json()
    return {
        "rating": data.get("imdbRating"),
        "reviews": [
            {"source": r.get("Source"), "value": r.get("Value")}
            for r in data.get("Ratings", [])
        ],
    }
