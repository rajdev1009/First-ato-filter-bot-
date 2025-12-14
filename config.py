import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get these from my.telegram.org
    # अगर आपने यहाँ सीधे नंबर डाले हैं, तो भी int() उसे संभाल लेगा
    API_ID = int(os.environ.get("API_ID", "1234567")) 
    API_HASH = os.environ.get("API_HASH", "your_hash_here")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token_here")

    # Database
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "your_mongo_url")

    # Channels (Direct ID dalne ke liye yahan change karein)
    # ध्यान दें: int() लगा रहने दें, और ID को ब्रैकेट के अंदर लिखें
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002795064458")) 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002746487551")) 
    PREMIUM_LOG_CHANNEL = int(os.environ.get("PREMIUM_LOG_CHANNEL", "-1002746487551")) 

    # Admin
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "123456789").split()]
    CREATOR_NAME = "Raj HD Movies"

    # Shortener
    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") 
