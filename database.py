from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "autofilter")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

files_col = db.files
users_col = db.users
settings_col = db.settings
bans_col = db.bans


# ───────────── FILES ─────────────
async def add_file(file_data: dict):
    await files_col.insert_one(file_data)


async def search_files(query, limit=10):
    cursor = files_col.find(
        {"file_name": {"$regex": query, "$options": "i"}}
    ).limit(limit)
    return await cursor.to_list(length=limit)


# ───────────── USERS ─────────────
async def add_user(user_id: int):
    if not await users_col.find_one({"_id": user_id}):
        await users_col.insert_one({"_id": user_id})


# ───────────── BANS ─────────────
async def ban_user(user_id: int):
    await bans_col.update_one(
        {"_id": user_id},
        {"$set": {"_id": user_id}},
        upsert=True
    )


async def unban_user(user_id: int):
    await bans_col.delete_one({"_id": user_id})


async def is_banned(user_id: int):
    return bool(await bans_col.find_one({"_id": user_id}))


# ───────────── STATS ─────────────
async def get_stats():
    users = await users_col.count_documents({})
    files = await files_col.count_documents({})
    return {"users": users, "files": files}


# ───────────── SHORTENER ─────────────
async def set_shortener(value: bool):
    await settings_col.update_one(
        {"_id": "shortener"},
        {"$set": {"value": value}},
        upsert=True
    )


async def get_shortener():
    data = await settings_col.find_one({"_id": "shortener"})
    return data["value"] if data else False
