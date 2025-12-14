import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")

    # यहाँ int() बहुत जरूरी है
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002795064458"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002746487551"))
    PREMIUM_LOG_CHANNEL = int(os.environ.get("PREMIUM_LOG_CHANNEL", "-1002746487551"))

    ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split()]
    CREATOR_NAME = "Raj HD Movies"

    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") 
