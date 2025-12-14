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

    # Channels (IDs must start with -100)
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "0"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))
    
    # Links (Update these!)
    UPDATE_CHANNEL_LINK = "https://t.me/+YZ7qQ1Ahx-M1MDdl" 
    MOVIE_GROUP_LINK = "https://t.me/+mgQzW_pjxT1hODI1"

    # Admins
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "0").split()]
    
