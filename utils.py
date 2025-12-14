import re
import aiohttp
from config import OMDB_API_KEY


# ───────────── CLEAN SEARCH QUERY ─────────────
def clean_query(text: str) -> str:
    """
    User input ko clean karke
    sirf movie / series ka naam return karta hai
    """
    text = text.lower()

    # remove years (1990–2099)
    text = re.sub(r"\b(19|20)\d{2}\b", "", text)

    # common unwanted words
    remove_words = [
        "480p", "720p", "1080p", "2160p",
        "hdrip", "webrip", "web-dl", "bluray",
        "hindi", "english", "dubbed",
        "full", "movie", "download"
    ]

    for word in remove_words:
        text = text.replace(word, "")

    # remove special characters
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ───────────── IMDB / OMDB SEARCH ─────────────
async def imdb_search(title: str):
    if not OMDB_API_KEY:
        return None

    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()
    except Exception:
        return None

    if data.get("Response") == "True":
        return {
            "title": data.get("Title"),
            "rating": data.get("imdbRating"),
            "plot": data.get("Plot"),
            "poster": data.get("Poster")
        }

    return None
