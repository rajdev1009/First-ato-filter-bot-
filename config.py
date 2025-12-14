import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API & Bot
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Database
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")

    # Channels (Integer Fix)
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "0"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))
    UPDATE_CHANNEL = int(os.environ.get("UPDATE_CHANNEL", "0"))

    # Links
    UPDATE_CHANNEL_LINK = "https://t.me/YOUR_UPDATE_LINK"
    MOVIE_GROUP_LINK = "https://t.me/Raj_Hd_movies"
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "RajHDAdmin") # Bina @ ke

    # Admin ID
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "0").split()]

    # Shortener (Optional)
    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") 
