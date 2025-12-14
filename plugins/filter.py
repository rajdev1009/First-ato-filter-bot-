import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

async def get_short_link(link):
    if not Config.SHORTENER_API:
        return link
    try:
        api_url = f"https://{Config.SHORTENER_URL}/api?api={Config.SHORTENER_API}&url={link}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
                return data.get("shortenedUrl", link)
    except:
        return link

@Client.on_message(filters.text & (filters.private | filters.group))
async def auto_filter(client, message):
    if message.text.startswith("/"):
        return

    status = await message.reply("⏳ Searching...")
    await asyncio.sleep(0.5)

    files = await db.search_files(message.text)
    if not files:
        return await status.edit("❌ No results found.")

    is_premium = await db.is_user_premium(message.from_user.id)
    settings = await db.get_settings()
    use_shortener = settings.get("shortener") and not is_premium

    buttons = []
    for file in files:
        if use_shortener:
            link = f"https://t.me/c/{str(Config.DB_CHANNEL).replace('-100','')}/{file['file_id']}"
            short = await get_short_link(link)
            buttons.append([InlineKeyboardButton(f"📁 {file['file_name']}", url=short)])
        else:
            buttons.append([InlineKeyboardButton(
                f"📁 {file['file_name']}",
                callback_data=f"file_{file['_id']}"
            )])

    if not is_premium:
        buttons.append([InlineKeyboardButton("💎 Buy Premium", callback_data="premium_price")])

    await status.edit(
        f"✅ Found {len(files)} results:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 🔥 PEER RESOLVE FIX (THIS SOLVES YOUR ERROR)
@Client.on_message(filters.channel & (filters.document | filters.video))
async def auto_save(client, message):
    if message.chat.id != Config.DB_CHANNEL:
        return
    await db.save_file(message)
    
