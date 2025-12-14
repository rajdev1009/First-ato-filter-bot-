from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired
from config import Config
from database import db
import asyncio

# --- INDEX COMMAND (Improved) ---
@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    # 1. Check if DB Channel is valid
    try:
        chat = await client.get_chat(Config.DB_CHANNEL)
        status_msg = await message.reply_text(f"✅ Found Channel: **{chat.title}**\n🔄 Connecting to DB...")
    except Exception as e:
        return await message.reply_text(f"❌ **Error:** I cannot access the DB Channel!\n\n**Reason:** {e}\n\n**Fix:** Make me Admin in the channel and send a message there.")

    # 2. Start Indexing
    total_indexed = 0
    try:
        async for msg in client.get_chat_history(Config.DB_CHANNEL):
            # Only process files (Video/Document)
            if msg.document or msg.video:
                saved = await db.save_file(msg)
                if saved:
                    total_indexed += 1
                
                # Show progress every 200 files
                if total_indexed % 200 == 0:
                    try:
                        await status_msg.edit_text(f"🔄 Indexing... **{total_indexed}** files saved.")
                    except:
                        pass # Edit limit error ignore
                        
    except ChatAdminRequired:
        await status_msg.edit_text("❌ **Error:** I need to be an **ADMIN** in the Database Channel to read history.")
        return
    except Exception as e:
        await status_msg.edit_text(f"❌ **Critical Error:** {e}")
        return

    await status_msg.edit_text(f"✅ **Indexing Complete!**\n💾 Total Files Saved: `{total_indexed}`")

# --- OTHER ADMIN COMMANDS ---
@Client.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats(client, message):
    users = await db.col.count_documents({})
    files = await db.files.count_documents({})
    await message.reply_text(f"📊 **Bot Statistics**\n\n👤 Users: `{users}`\n📂 Files: `{files}`")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, user_id, days = message.text.split()
        await db.add_premium(int(user_id), int(days))
        await message.reply_text(f"✅ User `{user_id}` is now Premium for `{days}` days.")
    except:
        await message.reply_text("Usage: `/add_premium USER_ID DAYS`")
        
