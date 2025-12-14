import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db

async def send_log(client, text):
    try:
        await client.send_message(Config.LOG_CHANNEL, text)
    except:
        pass

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    try:
        await client.get_chat(Config.DB_CHANNEL)
    except:
        return await message.reply("❌ DB Channel not synced. Send one file first.")

    await send_log(client, f"🚀 INDEX STARTED by {message.from_user.id}")
    status = await message.reply("🔄 Indexing...")

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
    await send_log(client, f"✅ INDEX COMPLETE\n📂 Total Saved: {saved}")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply("✅ Premium added")

        await send_log(
            client,
            f"💎 PREMIUM ADDED\n"
            f"👤 User: {uid}\n"
            f"⏳ Days: {days}\n"
            f"👮 By: {message.from_user.id}"
        )
    except:
        await message.reply("/add_premium USER_ID DAYS")
        
