from pyrogram import Client, filters
from config import Config
from database import db

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply("✅ Premium added")
    except:
        await message.reply("/add_premium USER_ID DAYS")
        
