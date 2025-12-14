import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get these from my.telegram.org
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Database
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")

    # Channels (must start with -100)
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "0")) # Files here
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) # Logs here
    PREMIUM_LOG_CHANNEL = int(os.environ.get("PREMIUM_LOG_CHANNEL", "0")) # Payment Proofs

    # Admin
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split()]
    CREATOR_NAME = "Raj HD Movies"

    # Shortener (Sotnar)
    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") 
