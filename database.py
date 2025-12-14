from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["autofilter"]

files = db.files
users = db.users
banned = db.banned


async def add_user(user_id):
    await users.update_one(
        {"_id": user_id},
        {"$set": {"_id": user_id}},
        upsert=True
    )


async def is_banned(user_id):
    return await banned.find_one({"_id": user_id}) is not None


async def count_files(query):
    return await files.count_documents(
        {"file_name": {"$regex": query, "$options": "i"}}
    )


async def search_files(query, skip, limit):
    cursor = files.find(
        {"file_name": {"$regex": query, "$options": "i"}}
    ).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
