import math
import asyncio
from pyrogram import Client, filters
from config import Config
from database import db

# Progress Bar Function
def get_progress_bar(current, total):
    pct = (current / total) * 100
    filled = int(pct / 10)
    bar = '▓' * filled + '░' * (10 - filled)
    return f"[{bar}] {round(pct, 2)}%"

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    status = await message.reply("🔄 **Connecting to DB Channel...**")
    
    # 1. Get Last Message ID (To calculate Percentage)
    try:
        last_msg = await client.send_message(Config.DB_CHANNEL, "🤖 Index Check")
        total_messages = last_msg.id
        await last_msg.delete()
    except Exception as e:
        return await status.edit(f"❌ **Error:** Cannot Access DB Channel.\nMake me **Admin** there.\n\nTrace: `{e}`")

    await status.edit(f"✅ Connection Established!\n📊 Total Messages to Scan: `{total_messages}`\n🚀 **Starting Index...**")

    # 2. Start Loop
    saved = 0
    curr_id = total_messages
    
    while curr_id > 0:
        try:
            # Batch of 200
            ids = list(range(curr_id, max(0, curr_id - 200), -1))
            msgs = await client.get_messages(Config.DB_CHANNEL, ids)
            
            for msg in msgs:
                if msg and (msg.document or msg.video):
                    if await db.save_file(msg):
                        saved += 1
                        
            curr_id -= 200
            
            # Update Progress every 200 files
            if curr_id % 200 == 0:
                bar = get_progress_bar(total_messages - curr_id, total_messages)
                await status.edit(f"🔄 **Indexing in Progress...**\n\n{bar}\n\n📂 Saved: `{saved}` files")

        except Exception as e:
            print(f"Index Skip: {e}")
            curr_id -= 200
            await asyncio.sleep(2)

    await status.edit(f"✅ **Indexing Completed!**\n\n💾 Total Files Saved: `{saved}`\n🗑 Scanned: `{total_messages}`")

# Toggle Shortener
@Client.on_message(filters.command("shortener") & filters.user(Config.ADMINS))
async def shortener_toggle(client, message):
    try:
        state = message.text.split()[1].lower() == "on"
        await db.update_shortener(state)
        await message.reply(f"Shortener is now: **{'ON' if state else 'OFF'}**")
    except: await message.reply("/shortener on | off")
        
