import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db

# 🔹 STATS COMMAND
# Shows how many users and files are in the database
@Client.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats(client, message):
    users = await db.col.count_documents({})
    files = await db.files.count_documents({})
    premium_users = await db.col.count_documents({'is_premium': True})
    
    text = (
        f"**📊 Bot Statistics**\n\n"
        f"👤 Total Users: `{users}`\n"
        f"💎 Premium Users: `{premium_users}`\n"
        f"📂 Total Files: `{files}`\n"
        f"💾 Storage Used: (MongoDB Limit)"
    )
    await message.reply_text(text)

# 🔹 BROADCAST COMMAND
# Sends a message to all users in the database
@Client.on_message(filters.command("broadcast") & filters.reply & filters.user(Config.ADMINS))
async def broadcast(client, message):
    status_msg = await message.reply_text("📣 Broadcast Started...")
    all_users = db.col.find({})
    
    success = 0
    failed = 0
    
    async for user in all_users:
        try:
            await message.reply_to_message.copy(user['id'])
            success += 1
            await asyncio.sleep(0.3) # Prevent FloodWait
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(user['id'])
        except Exception:
            failed += 1
            
    await status_msg.edit_text(f"✅ Broadcast Complete\n\nSent: {success}\nFailed: {failed}")

# 🔹 INDEX COMMAND
# This saves ALL existing files from the DB Channel to MongoDB
@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index_channel(client, message):
    status_msg = await message.reply_text(f"🔄 Indexing started for Channel: `{Config.DB_CHANNEL}`...")
    
    total_indexed = 0
    try:
        async for msg in client.get_chat_history(Config.DB_CHANNEL):
            if msg.document or msg.video:
                # Reuse the save function from database.py
                await db.save_file(msg)
                total_indexed += 1
                
                if total_indexed % 100 == 0:
                    await status_msg.edit_text(f"🔄 Indexing... {total_indexed} files saved.")
                    
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        
    await status_msg.edit_text(f"✅ Indexing Completed!\nTotal Files: {total_indexed}")
  
