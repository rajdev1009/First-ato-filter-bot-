import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

async def send_log(client, text):
    try:
        await client.send_message(Config.LOG_CHANNEL, text)
    except:
        pass

@Client.on_message(filters.text & (filters.private | filters.group))
async def auto_filter(client, message):
    if message.text.startswith("/"): return
    await send_log(client, f"🔍 SEARCH {message.from_user.id}: {message.text}")
    files = await db.search_files(message.text)
    if not files:
        await send_log(client, "❌ No results")
        return await message.reply("❌ No results found.")
    buttons = [
        [InlineKeyboardButton(f"📁 {file['file_name']}", callback_data=f"file_{file['_id']}")]
        for file in files
    ]
    buttons.append([InlineKeyboardButton("💎 Buy Premium", callback_data="premium_price")])
    await message.reply("✅ Found results", reply_markup=InlineKeyboardMarkup(buttons))
    await send_log(client, f"✅ Sent {len(files)} results to {message.from_user.id}")

@Client.on_message(filters.channel & (filters.document | filters.video))
async def auto_save(client, message):
    if message.chat.id != Config.DB_CHANNEL: return
    saved = await db.save_file(message)
    if saved:
        await send_log(client, f"📥 FILE SAVED: {message.caption or 'No Caption'}")
        
