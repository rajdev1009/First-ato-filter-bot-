import os
import ast

# ───────────── TELEGRAM ─────────────
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ───────────── DATABASE ─────────────
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "AutoFilterBot")

# ───────────── ADMINS ─────────────
ADMINS = ast.literal_eval(
    os.getenv("ADMINS", "[]")
)

# ───────────── OMDB / IMDB ─────────────
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# ───────────── BOT SETTINGS ─────────────
RESULTS_PER_PAGE = int(os.getenv("RESULTS_PER_PAGE", 10))
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", 600))
