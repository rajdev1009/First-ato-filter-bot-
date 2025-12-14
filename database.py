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

    # --- User & Premium ---
    async def add_user(self, id, name):
        user = await self.col.find_one({'id': id})
        if not user:
            await self.col.insert_one({'id': id, 'name': name, 'is_premium': False, 'expiry': None})
            return True
        return False

    async def is_user_premium(self, id):
        user = await self.col.find_one({'id': id})
        if user and user.get('is_premium'):
            if user.get('expiry') and user['expiry'] < datetime.datetime.now():
                await self.remove_premium(id) # Smart Atomic Cut
                return False
            return True
        return False

    async def add_premium(self, id, days):
        expiry = datetime.datetime.now() + datetime.timedelta(days=int(days))
        await self.col.update_one({'id': id}, {'$set': {'is_premium': True, 'expiry': expiry}}, upsert=True)

    async def remove_premium(self, id):
        await self.col.update_one({'id': id}, {'$set': {'is_premium': False, 'expiry': None}})

    # --- Files (No Duplicates) ---
    async def save_file(self, message):
        try:
            file_id = message.id
            if await self.files.find_one({'file_id': file_id}):
                return False # Duplicate found
            
            media = message.document or message.video or message.audio
            file_name = message.caption or (media.file_name if media else "Unknown")
            # Create Direct Link
            link = f"https://t.me/c/{str(Config.DB_CHANNEL).replace('-100', '')}/{message.id}"
            
            await self.files.insert_one({
                'file_name': file_name.lower(),
                'file_id': file_id,
                'caption': message.caption,
                'link': link
            })
            return True
        except Exception as e:
            print(f"Save Error: {e}")
            return False

    async def search_files(self, query):
        regex = {"$regex": query, "$options": "i"}
        return await self.files.find({"file_name": regex}).limit(10).to_list(length=10)

    # --- Settings ---
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
