from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db
import asyncio

# --- NEW FORCE INDEX METHOD ---
@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    # 1. Check Access & Find Last Message ID
    status = await message.reply_text("🔄 **Connecting to DB Channel...**")
    
    try:
        # हम एक डमी मैसेज भेजकर चेक करेंगे कि आखिरी मैसेज नंबर क्या है
        test_msg = await client.send_message(Config.DB_CHANNEL, "🤖 Indexing Check...")
        last_msg_id = test_msg.id
        await test_msg.delete() # डिलीट कर देंगे
    except Exception as e:
        return await status.edit_text(f"❌ **Error:** I cannot send messages to DB Channel.\nMake sure I am Admin there.\n\nTrace: {e}")

    await status.edit_text(f"✅ Access Granted!\n🔢 Last Message ID is: `{last_msg_id}`\n🚀 **Starting Indexing by ID...**")

    # 2. Start Loop (ID 1 se Last ID tak)
    total_indexed = 0
    try:
        # हम हिस्ट्री नहीं मांगेंगे, सीधा नंबर से मैसेज उठाएंगे (Batch of 200)
        # यह method कभी 'BOT_METHOD_INVALID' नहीं देता
        current_id = last_msg_id
        
        while current_id > 0:
            try:
                # 200 messages ka batch ek sath uthao
                # E.g., agar last ID 1000 hai, to 1000 se 800 tak layega
                ids = list(range(current_id, max(0, current_id - 200), -1))
                messages = await client.get_messages(Config.DB_CHANNEL, ids)
                
                for msg in messages:
                    if msg and (msg.document or msg.video):
                        if await db.save_file(msg):
                            total_indexed += 1
                
                current_id -= 200 # peeche jao
                
                # Update status every 200 messages
                if total_indexed % 200 == 0:
                    await status.edit_text(f"🔄 Scanning... Last scanned ID: {current_id}\n💾 Saved: {total_indexed}")
                
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"Skipping batch: {e}")
                current_id -= 200
                
    except Exception as e:
        await status.edit_text(f"❌ Critical Error: {e}")
        return

    await status.edit_text(f"✅ **Indexing Completed!**\n💾 Total Files Saved: `{total_indexed}`")

# --- OTHER ADMIN COMMANDS (Same as before) ---
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
        
