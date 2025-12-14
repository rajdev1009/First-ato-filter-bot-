import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get these from my.telegram.org
    API_ID = int(os.environ.get("API_ID", "1234567"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

    # Database
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "your_mongodb_url")

    # Channels (Use -100xxxxxx IDs)
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-100xxxx")) # Where files are
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-100xxxx")) # User logs
    PREMIUM_LOG_CHANNEL = int(os.environ.get("PREMIUM_LOG_CHANNEL", "-100xxxx")) # Payment logs

    # Admin
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "12345678").split()]
    CREATOR_NAME = "Raj HD Movies"

    # Shortener (Sotnar)
    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") # e.g., "shortener.com"
