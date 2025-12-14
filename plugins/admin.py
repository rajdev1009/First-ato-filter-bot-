import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db

def get_progress(current, total):
    pct = (current / total) * 100
    filled = int(pct / 10)
    bar = '▓' * filled + '░' * (10 - filled)
    return f"{bar} {round(pct, 1)}%"

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    status = await message.reply("🔄 **Connecting...**")
    try:
        last_msg = await client.send_message(Config.DB_CHANNEL, "🤖 Index Check")
        total_ids = last_msg.id
        await last_msg.delete()
    except Exception as e:
        return await status.edit(f"❌ Error: Cannot connect to DB Channel.\nTrace: `{e}`")

    await status.edit(f"✅ Connection OK!\n📥 Total: `{total_ids}`\n🚀 **Starting Smooth Index...**")

    current_id = total_ids
    saved_count = 0
    batch_size = 50 

    while current_id > 0:
        try:
            ids = list(range(current_id, max(0, current_id - batch_size), -1))
            messages = await client.get_messages(Config.DB_CHANNEL, ids)

            for msg in messages:
                if msg and not msg.empty and (msg.document or msg.video):
                    if await db.save_file(msg): saved_count += 1
            
            current_id -= batch_size

            if current_id % 200 == 0:
                bar = get_progress(total_ids - current_id, total_ids)
                try: await status.edit(f"🔄 **Indexing...**\n{bar}\n📂 Saved: `{saved_count}`")
                except: pass
            
            await asyncio.sleep(1.5) 

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            current_id -= batch_size

    await status.edit(f"✅ **Indexing Completed!**\n💾 Saved: `{saved_count}` files.")

@Client.on_message(filters.command("shortener") & filters.user(Config.ADMINS))
async def shortener_toggle(client, message):
    try:
        state = message.text.split()[1].lower() == "on"
        await db.update_shortener(state)
        await message.reply(f"Shortener: **{'ON' if state else 'OFF'}**")
    except: await message.reply("/shortener on | off")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply(f"✅ Premium added.")
    except: await message.reply("/add_premium ID DAYS")
        
