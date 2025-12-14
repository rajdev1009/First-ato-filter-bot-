from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db
import asyncio

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    status = await message.reply_text("🔄 **Checking Access...**")
    try:
        test = await client.send_message(Config.DB_CHANNEL, "🤖 Index Check")
        last_id = test.id
        await test.delete()
    except Exception as e:
        return await status.edit_text(f"❌ Error: Make me ADMIN in DB Channel.\n\n{e}")

    await status.edit_text(f"✅ Access OK. Indexing till ID: {last_id}")
    
    total = 0
    curr_id = last_id
    while curr_id > 0:
        try:
            ids = list(range(curr_id, max(0, curr_id - 200), -1))
            msgs = await client.get_messages(Config.DB_CHANNEL, ids)
            for msg in msgs:
                if msg and (msg.document or msg.video):
                    if await db.save_file(msg): total += 1
            curr_id -= 200
            if total % 200 == 0: await status.edit_text(f"Indexed: {total} files...")
        except FloodWait as e: await asyncio.sleep(e.value)
        except: curr_id -= 200
        
    await status.edit_text(f"✅ **Done!** Total Saved: {total}")
    
