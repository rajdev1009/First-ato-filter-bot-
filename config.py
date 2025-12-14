import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Database
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")

    # Channels (Auto-Convert to Integer)
    # अगर आपने गलती से "" लगा दिया है, तो यह उसे हटाकर नंबर बना देगा
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002795064458"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002746487551"))
    PREMIUM_LOG_CHANNEL = int(os.environ.get("PREMIUM_LOG_CHANNEL", "-1002746487551"))

    # Admin
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "0").split()]
    CREATOR_NAME = "Raj HD Movies"

    # Shortener
    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") 
