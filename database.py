import motor.motor_asyncio
import datetime
from config import Config

class Database:
    def __init__(self, uri, database_name):
        # Connect to MongoDB
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        
        # Collections
        self.col = self.db.users
        self.files = self.db.files
        self.settings = self.db.settings

    # ------------------ USER & PREMIUM SYSTEM ------------------

    async def add_user(self, id, name):
        """Adds a new user to database if not exists"""
        user = await self.col.find_one({'id': id})
        if not user:
            await self.col.insert_one({
                'id': id, 
                'name': name, 
                'is_premium': False, 
                'expiry': None
            })
            return True
        return False

    async def is_user_premium(self, id):
        """Checks if user is premium AND if plan is valid (Smart Atomic Cut)"""
        user = await self.col.find_one({'id': id})
        if user and user.get('is_premium'):
            # Check if expiry date has passed
            expiry = user.get('expiry')
            if expiry and expiry < datetime.datetime.now():
                # Plan expired: Remove premium automatically
                await self.remove_premium(id)
                return False
            return True
        return False

    async def add_premium(self, id, days):
        """Activates premium for X days"""
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=int(days))
        await self.col.update_one(
            {'id': id}, 
            {'$set': {'is_premium': True, 'expiry': expiry_date}}, 
            upsert=True
        )

    async def remove_premium(self, id):
        """Removes premium status"""
        await self.col.update_one(
            {'id': id}, 
            {'$set': {'is_premium': False, 'expiry': None}}
        )

    # ------------------ FILE MANAGEMENT (AUTO SAVE) ------------------

    async def save_file(self, message):
        """Saves file to MongoDB. Returns True if saved, False if duplicate."""
        try:
            file_id = message.id  # The message ID in the DB Channel
            
            # 1. DUPLICATE CHECK: If file_id exists, stop.
            if await self.files.find_one({'file_id': file_id}):
                return False 

            # 2. Get File Name (Handle Document, Video, or Audio)
            media = message.document or message.video or message.audio
            file_name = message.caption or (media.file_name if media else "Unknown_File")
            
            # 3. Generate Direct Link (Stream Link Format)
            # Removes "-100" from channel ID to make a valid deep link
            channel_id_str = str(Config.DB_CHANNEL).replace("-100", "")
            link = f"https://t.me/c/{channel_id_str}/{message.id}"
            
            # 4. Save to DB
            file_data = {
                'file_name': file_name.lower(), # Lowercase helps in search
                'file_id': file_id,
                'caption': message.caption,
                'file_type': 'video' if message.video else 'document',
                'link': link
            }
            await self.files.insert_one(file_data)
            return True
            
        except Exception as e:
            print(f"Error in save_file: {e}")
            return False

    async def search_files(self, query):
        """Searches for files by name (Regex)"""
        # "i" option means case-insensitive (Avengers = avengers)
        regex = {"$regex": query, "$options": "i"}
        cursor = self.files.find({"file_name": regex})
        # Return top 10 results
        return await cursor.to_list(length=10)

    # ------------------ SETTINGS (SHORTENER & PM) ------------------

    async def get_settings(self):
        """Gets current bot settings"""
        settings = await self.settings.find_one({'id': 'master'})
        if not settings:
            # Default settings if not set
            default = {'shortener': True, 'pm_search': True}
            await self.settings.insert_one({'id': 'master', **default})
            return default
        return settings

    async def update_setting(self, key, value):
        """Updates a specific setting (e.g., shortener off)"""
        await self.settings.update_one(
            {'id': 'master'}, 
            {'$set': {key: value}}, 
            upsert=True
        )

# Initialize Database
db = Database(Config.MONGO_DB_URI, "RajHDMoviesBot")
