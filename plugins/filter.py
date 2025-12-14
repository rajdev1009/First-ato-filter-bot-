from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

@Client.on_message(filters.chat(Config.DB_CHANNEL) & (filters.document | filters.video))
async def auto_save(client, message):
    if await db.save_file(message):
        print(f"✅ Saved File: {message.id}")

@Client.on_message(filters.text & (filters.private | filters.group))
async def auto_filter(client, message):
    if message.text.startswith("/"): return

    # LOGGING
    try:
        log_text = f"🔍 **Search:** `{message.text}`\n👤 **User:** {message.from_user.mention}\n📍 **Chat:** {message.chat.title or 'Private'}"
        await client.send_message(Config.LOG_CHANNEL, log_text)
        print(f"Search Log: {message.text}")
    except: pass

    files = await db.search_files(message.text)
    if not files:
        if message.chat.type == "private":
            await message.reply("❌ No results found.")
        return

    btn = []
    for file in files:
        btn.append([InlineKeyboardButton(f"📁 {file['file_name']}", callback_data=f"file_{file['_id']}")])

    await message.reply_text(f"✅ **Found {len(files)} results:**", reply_markup=InlineKeyboardMarkup(btn))
    
