import motor.motor_asyncio
import datetime
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.files = self.db.files
        self.settings = self.db.settings

    # --- User Management ---
    async def add_user(self, id, name):
        user = await self.col.find_one({'id': id})
        if not user:
            await self.col.insert_one({'id': id, 'name': name, 'is_premium': False, 'expiry': None})
            return True
        return False

    async def is_user_premium(self, id):
        user = await self.col.find_one({'id': id})
        if user and user.get('is_premium'):
            # Smart Atomic Cut: Check expiry
            if user['expiry'] and user['expiry'] < datetime.datetime.now():
                await self.remove_premium(id)
                return False
            return True
        return False

    async def add_premium(self, id, days):
        expiry = datetime.datetime.now() + datetime.timedelta(days=int(days))
        await self.col.update_one({'id': id}, {'$set': {'is_premium': True, 'expiry': expiry}})

    async def remove_premium(self, id):
        await self.col.update_one({'id': id}, {'$set': {'is_premium': False, 'expiry': None}})

    # --- File Management (Auto Save) ---
    async def save_file(self, message):
        # Stores file_id, caption, and message_id for linking
        file_name = message.caption or message.document.file_name or "Unknown"
        file = {
            'file_name': file_name.lower(),
            'file_id': message.id, # Message ID in DB Channel
            'caption': message.caption,
            'link': f"https://t.me/c/{str(Config.DB_CHANNEL)[4:]}/{message.id}"
        }
        await self.files.insert_one(file)

    async def search_files(self, query):
        # Returns 5-10 results based on regex
        regex = {"$regex": query, "$options": "i"}
        return await self.files.find({"file_name": regex}).limit(10).to_list(length=10)

    # --- Settings (Shortener/PM Search) ---
    async def get_settings(self):
        settings = await self.settings.find_one({'id': 'master'})
        if not settings:
            default = {'shortener': True, 'pm_search': True}
            await self.settings.insert_one({'id': 'master', **default})
            return default
        return settings

    async def update_setting(self, key, value):
        await self.settings.update_one({'id': 'master'}, {'$set': {key: value}}, upsert=True)

db = Database(Config.MONGO_DB_URI, "RajHDMoviesBot")
