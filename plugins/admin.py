import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db

def get_progress(current, total):
    pct = (current / total) * 100
    filled = int(pct / 10)
    bar = "▓" * filled + "░" * (10 - filled)
    return f"{bar} {round(pct,1)}%"

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    try:
        await client.get_chat(Config.DB_CHANNEL)
    except:
        return await message.reply(
            "❌ DB Channel not synced.\n"
            "👉 Send ONE video/document in DB channel first."
        )

    status = await message.reply("🔄 Starting Index...")
    saved = 0

    async for msg in client.get_chat_history(Config.DB_CHANNEL):
        try:
            if msg.document or msg.video:
                if await db.save_file(msg):
                    saved += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            pass

    await status.edit(f"✅ Index Complete\n📂 Saved: {saved}")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply("✅ Premium added")
    except:
        await message.reply("/add_premium USER_ID DAYS")
        
