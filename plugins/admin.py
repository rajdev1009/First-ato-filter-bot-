from pyrogram import Client, filters
from config import Config
from database import db
import asyncio

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    msg = await message.reply("Indexing started...")
    count = 0
    try:
        async for m in client.get_chat_history(Config.DB_CHANNEL):
            if m.document or m.video:
                if await db.save_file(m): count += 1
    except Exception as e:
        await msg.edit(f"Error: {e}")
        return
    await msg.edit(f"✅ Indexed {count} new files.")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply("Premium Added.")
        await client.send_message(Config.PREMIUM_LOG_CHANNEL, f"User {uid} added for {days} days.")
    except: await message.reply("/add_premium ID DAYS")

@Client.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats(client, message):
    users = await db.col.count_documents({})
    files = await db.files.count_documents({})
    await message.reply(f"Users: {users}\nFiles: {files}")

@Client.on_message(filters.command("shortener") & filters.user(Config.ADMINS))
async def toggle_short(client, message):
    try:
        state = message.text.split()[1].lower() == 'on'
        await db.update_setting('shortener', state)
        await message.reply(f"Shortener: {state}")
    except: await message.reply("/shortener on/off")
        
