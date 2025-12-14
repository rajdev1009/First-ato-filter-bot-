import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

async def get_short_link(link):
    if not Config.SHORTENER_API: return link
    try:
        api_url = f"https://{Config.SHORTENER_URL}/api?api={Config.SHORTENER_API}&url={link}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
                return data.get('shortenedUrl', link)
    except: return link

@Client.on_message(filters.chat(Config.DB_CHANNEL) & (filters.document | filters.video))
async def auto_save(client, message):
    await db.save_file(message)

@Client.on_message(filters.text & filters.private)
async def auto_filter(client, message):
    if message.text.startswith("/"): return
    
    settings = await db.get_settings()
    if not settings['pm_search'] and message.from_user.id not in Config.ADMINS:
        return await message.reply("PM Search OFF.")

    files = await db.search_files(message.text)
    if not files: return await message.reply("No results found.")

    is_premium = await db.is_user_premium(message.from_user.id)
    use_shortener = settings['shortener'] and not is_premium

    btn = []
    for file in files:
        link = await get_short_link(file['link']) if use_shortener else file['link']
        btn.append([InlineKeyboardButton(f"📁 {file['file_name']}", url=link)])

    if not is_premium:
        btn.append([InlineKeyboardButton("💎 Buy Premium (No Ads)", callback_data="premium_price")])

    await message.reply_text(f"Found {len(files)} results:", reply_markup=InlineKeyboardMarkup(btn))
    
