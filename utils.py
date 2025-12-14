import re
import aiohttp

def clean_query(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


async def imdb_search(query):
    return None  # abhi skip, error nahi aayega
