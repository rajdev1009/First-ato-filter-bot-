import os

# ───────────── TELEGRAM ─────────────
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ───────────── DATABASE ─────────────
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = "AutoFilterBot"

# ───────────── ADMINS ─────────────
# Example: ADMINS="123456789 987654321"
ADMINS = list(
    map(
        int,
        os.getenv("ADMINS", "").split()
    )
)

# ───────────── BOT SETTINGS ─────────────
RESULTS_PER_PAGE = 10          # pagination limit
AUTO_DELETE_TIME = 600         # 10 minutes

# ───────────── IMDB / OMDB ─────────────
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")

# ───────────── FORCE SUBSCRIBE ─────────────
# Example: FORCE_SUB="YourChannelUsername"
FORCE_SUB = os.getenv("FORCE_SUB", "")
