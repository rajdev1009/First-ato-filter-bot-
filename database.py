from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME

# ───────────── Mongo Client ─────────────
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]

# ───────────── Collections ─────────────
files_col = db.files       # indexed files
users_col = db.users       # users & ban
settings_col = db.settings # bot settings
stats_col = db.stats       # statistics


# ───────────── INIT DB ─────────────
async def init_db():
    # settings
    await settings_col.update_one(
        {"_id": "bot"},
        {"$setOnInsert": {
            "shortener": False,
            "force_sub": False
        }},
        upsert=True
    )

    # stats
    await stats_col.update_one(
        {"_id": "stats"},
        {"$setOnInsert": {
            "users": 0,
            "files": 0
        }},
        upsert=True
    )


# ───────────── USERS ─────────────
async def add_user(user_id: int):
    user = await users_col.find_one({"_id": user_id})
    if not user:
        await users_col.insert_one({
            "_id": user_id,
            "banned": False
        })
        await stats_col.update_one(
            {"_id": "stats"},
            {"$inc": {"users": 1}}
        )


async def is_banned(user_id: int) -> bool:
    user = await users_col.find_one({"_id": user_id})
    return user["banned"] if user else False


async def ban_user(user_id: int):
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"banned": True}},
        upsert=True
    )


async def unban_user(user_id: int):
    await users_col.update_one(
        {"_id": user_id},
        {"$set": {"banned": False}}
    )


# ───────────── FILES ─────────────
async def add_file(file_data: dict):
    """
    file_data keys:
    file_id, file_name, file_size, chat_id, message_id
    """
    result = await files_col.update_one(
        {"file_id": file_data["file_id"]},
        {"$set": file_data},
        upsert=True
    )

    if result.upserted_id:
        await stats_col.update_one(
            {"_id": "stats"},
            {"$inc": {"files": 1}}
        )


async def get_file(file_id: str):
    return await files_col.find_one({"file_id": file_id})


async def search_files(query: str, skip: int, limit: int):
    return await files_col.find(
        {"file_name": {"$regex": query, "$options": "i"}}
    ).sort("file_size", -1).skip(skip).limit(limit).to_list(length=limit)


async def count_files(query: str) -> int:
    return await files_col.count_documents(
        {"file_name": {"$regex": query, "$options": "i"}}
    )


# ───────────── SETTINGS ─────────────
async def get_settings():
    return await settings_col.find_one({"_id": "bot"})


async def set_shortener(value: bool):
    await settings_col.update_one(
        {"_id": "bot"},
        {"$set": {"shortener": value}}
    )


# ───────────── STATS ─────────────
async def get_stats():
    return await stats_col.find_one({"_id": "stats"})
