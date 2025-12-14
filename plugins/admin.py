import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import db

# --- PROGRESS BAR ---
def get_progress(current, total):
    pct = (current / total) * 100
    filled = int(pct / 10)
    bar = '▓' * filled + '░' * (10 - filled)
    return f"{bar} {round(pct, 1)}%"

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def index(client, message):
    status = await message.reply("🔄 **Connecting to DB Channel...**")
    
    # 1. Check & Get Last ID
    try:
        # Ek dummy message bhej kar check karenge
        last_msg = await client.send_message(Config.DB_CHANNEL, "🤖 Index Check")
        total_ids = last_msg.id
        await last_msg.delete()
    except Exception as e:
        return await status.edit(f"❌ **Connection Failed!**\n\nMake sure Bot is **Admin** in DB Channel.\nTrace: `{e}`")

    await status.edit(f"✅ Connection OK!\n📥 Total Messages to Scan: `{total_ids}`\n🚀 **Starting Index...**")

    # 2. Start Loop (New Method: ID Iterator)
    current_id = total_ids
    saved_count = 0
    batch_size = 50 # Chota batch taaki fast update ho

    while current_id > 0:
        try:
            # Batch of 50 IDs
            ids = list(range(current_id, max(0, current_id - batch_size), -1))
            
            # Method change: get_chat_history HATAYA -> get_messages LAGAYA
            messages = await client.get_messages(Config.DB_CHANNEL, ids)

            for msg in messages:
                if msg and not msg.empty and (msg.document or msg.video):
                    if await db.save_file(msg):
                        saved_count += 1
            
            current_id -= batch_size

            # Update Progress every 100 messages
            if current_id % 100 == 0:
                bar = get_progress(total_ids - current_id, total_ids)
                try:
                    await status.edit(
                        f"🔄 **Indexing in Progress...**\n"
                        f"{bar}\n\n"
                        f"📂 Saved: `{saved_count}` files\n"
                        f"🔍 Scanning ID: `{current_id}`"
                    )
                except: pass

        except FloodWait as e:
            # 🛑 Agar Telegram roke, to User ko batao
            try:
                await status.edit(f"😴 **Telegram High Traffic!**\nSleeping for {e.value} seconds...\n(Don't worry, I will resume automatically)")
            except: pass
            await asyncio.sleep(e.value) # So jao
        
        except Exception as e:
            print(f"Skipping Batch: {e}")
            current_id -= batch_size

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
        
