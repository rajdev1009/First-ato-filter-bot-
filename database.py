from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "autofilter")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

files_col = db.files


async def add_file(file_id, file_name, file_size, caption, file_type):
    data = {
        "file_id": file_id,
        "file_name": file_name.lower(),
        "file_size": file_size,
        "caption": caption,
        "file_type": file_type
    }
    await files_col.insert_one(data)


async def search_files(query, limit=10):
    cursor = files_col.find(
        {"file_name": {"$regex": query, "$options": "i"}}
    ).limit(limit)

    return await cursor.to_list(length=limit)


async def get_files_count():
    return await files_col.count_documents({})
