import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db

# --- PROGRESS BAR FUNCTION ---
def get_progress_bar(current, total):
    pct = (current / total) * 100
    filled = int(pct / 10)
    bar = '▓' * filled + '░' * (10 - filled)
    return f"{bar} {round(pct, 1)}%"

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    # 1. Connection Check
    status = await message.reply("🔄 **Connecting...**")
    try:
        last_msg = await client.send_message(Config.DB_CHANNEL, "🤖 Index Check")
        total_ids = last_msg.id
        await last_msg.delete()
    except Exception as e:
        return await status.edit(f"❌ **Error:** I cannot connect to DB Channel.\nMake me **Admin** there.\nTrace: `{e}`")

    await status.edit(f"✅ Connection OK!\n📥 Total Messages: `{total_ids}`\n🚀 **Starting Fast Index...**")
    
    # 2. Indexing Loop
    current_id = total_ids
    saved_count = 0
    batch_size = 50  # Chota batch taaki update fast ho

    while current_id > 0:
        try:
            # Batch calculate karein
            start = current_id
            end = max(0, current_id - batch_size)
            ids = list(range(start, end, -1))

            # Messages fetch karein
            messages = await client.get_messages(Config.DB_CHANNEL, ids)

            for msg in messages:
                # Agar message empty nahi hai aur File hai
                if msg and not msg.empty and (msg.document or msg.video):
                    if await db.save_file(msg):
                        saved_count += 1

            # Agla batch
            current_id -= batch_size

            # Status Update (Har 100 message ya 2 batch ke baad)
            if current_id % 100 == 0:
                percent = get_progress_bar(total_ids - current_id, total_ids)
                try:
                    await status.edit(
                        f"🔄 **Indexing...**\n"
                        f"{percent}\n"
                        f"📂 Saved: `{saved_count}`\n"
                        f"🔍 Scanning ID: `{current_id}`"
                    )
                except:
                    pass # Edit error ignore karein
            
            # Koyeb Log (Taaki pata chale bot zinda hai)
            print(f"Scanned till ID: {current_id} | Saved: {saved_count}")

        except FloodWait as e:
            # 🛑 Agar Telegram roke, to user ko batao
            print(f"⚠️ FloodWait: Sleeping {e.value}s")
            try:
                await status.edit(f"😴 **Telegram told me to sleep for {e.value}s...**\n(Don't worry, I will resume automatically)")
            except: pass
            await asyncio.sleep(e.value)
        
        except Exception as e:
            print(f"Error skipping batch: {e}")
            current_id -= batch_size # Error aaye to bhi aage badho, ruko mat

    await status.edit(f"✅ **Indexing Completed!**\n\n💾 Total Files Saved: `{saved_count}`\n🗑 Scanned IDs: `{total_ids}`")

# --- OTHER COMMANDS ---
@Client.on_message(filters.command("shortener") & filters.user(Config.ADMINS))
async def shortener_toggle(client, message):
    try:
        state = message.text.split()[1].lower() == "on"
        await db.update_shortener(state)
        await message.reply(f"Shortener is now: **{'ON' if state else 'OFF'}**")
    except: await message.reply("/shortener on | off")

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium(client, message):
    try:
        _, uid, days = message.text.split()
        await db.add_premium(int(uid), int(days))
        await message.reply(f"✅ Premium added to {uid} for {days} days.")
    except: await message.reply("Use: `/add_premium ID DAYS`")
        
