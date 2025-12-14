import motor.motor_asyncio
import datetime
from bson.objectid import ObjectId
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.files = self.db.files
        self.settings = self.db.settings

    async def add_user(self, id, name):
        if not await self.col.find_one({'id': id}):
            await self.col.insert_one({'id': id, 'name': name, 'is_premium': False})

    async def is_user_premium(self, id):
        user = await self.col.find_one({'id': id})
        if user and user.get('is_premium'):
            if user.get('expiry') and user['expiry'] < datetime.datetime.utcnow():
                await self.col.update_one({'id': id}, {'$set': {'is_premium': False}})
                return False
            return True
        return False

    async def add_premium(self, id, days):
        expiry = datetime.datetime.utcnow() + datetime.timedelta(days=int(days))
        await self.col.update_one({'id': id}, {'$set': {'is_premium': True, 'expiry': expiry}}, upsert=True)

    async def save_file(self, message):
        try:
            file_id = message.id
            if await self.files.find_one({'file_id': file_id}): return False 
            media = message.document or message.video or message.audio
            if not media: return False
            file_name = message.caption or getattr(media, "file_name", "Unknown")
            await self.files.insert_one({
                'file_name': file_name.lower(),
                'file_id': file_id,
                'caption': message.caption,
                'file_type': 'video' if message.video else 'document'
            })
            return True
        except: return False

    async def search_files(self, query):
        regex = {"$regex": query, "$options": "i"}
        return await self.files.find({"file_name": regex}).limit(10).to_list(length=10)

    async def get_file(self, _id):
        try:
            return await self.files.find_one({"_id": ObjectId(_id)})
        except: return None

    async def get_settings(self):
        settings = await self.settings.find_one({'id': 'master'})
        if not settings:
            await self.settings.insert_one({'id': 'master', 'shortener': False})
            return {'shortener': False}
        return settings

    async def update_shortener(self, status):
        await self.settings.update_one({'id': 'master'}, {'$set': {'shortener': status}}, upsert=True)

db = Database(Config.MONGO_DB_URI, "Raj_Pro_Bot_Final")
