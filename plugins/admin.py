from pyrogram import Client, filters
from config import Config
from database import db

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    status = await message.reply_text("🔄 **Checking Channel Access...**")
    
    # Step 1: Check Connection
    try:
        chat = await client.get_chat(Config.DB_CHANNEL)
    except Exception as e:
        return await status.edit_text(f"❌ **Error:** I cannot access the DB Channel.\n\nMake sure I am **Admin** in the channel and you have sent a 'Hello' message there.\n\nTrace: {e}")

    # Step 2: Start Indexing
    await status.edit_text(f"✅ Connected to: **{chat.title}**\n📂 Starting Indexing...")
    
    total = 0
    try:
        async for msg in client.get_chat_history(Config.DB_CHANNEL):
            if msg.document or msg.video:
                if await db.save_file(msg):
                    total += 1
                if total % 200 == 0:
                    try: await status.edit_text(f"Indexed: {total} files...")
                    except: pass
    except Exception as e:
        return await status.edit_text(f"❌ Error while reading files: {e}")
        
    await status.edit_text(f"✅ **Indexing Completed!**\n💾 Total Saved: {total}")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply(f"✅ User {uid} added for {days} days.")
    except: await message.reply("/add_premium ID DAYS")
        
