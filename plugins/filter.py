import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

# Helper function for Shortener
async def get_short_link(link):
    url = Config.SHORTENER_URL
    api = Config.SHORTENER_API
    try:
        # Example API format (change according to your shortener service)
        api_url = f"https://{url}/api?api={api}&url={link}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
                return data['shortenedUrl']
    except:
        return link # Fallback to original if error

# 🔹 AUTO SAVE FEATURE
# Listens to DB Channel and saves files automatically
@Client.on_message(filters.chat(Config.DB_CHANNEL) & (filters.document | filters.video))
async def auto_save(client, message):
    await db.save_file(message)
    # Optional: Edit message to say "Saved"
    # await message.edit_caption(f"{message.caption}\n\n✅ Indexed")

# 🔹 AUTO FILTER & SEARCH
@Client.on_message(filters.text & filters.private)
async def auto_filter(client, message):
    query = message.text
    settings = await db.get_settings()

    # PM Search Check
    if not settings['pm_search'] and message.from_user.id not in Config.ADMINS:
        return await message.reply("PM Search is currently OFF.")

    files = await db.search_files(query)
    if not files:
        return await message.reply("No results found. Try another name.")

    # Check Premium Status
    is_premium = await db.is_user_premium(message.from_user.id)
    use_shortener = settings['shortener'] and not is_premium

    btn = []
    for file in files:
        link = file['link']
        
        # SOTNAR (Shortener) LOGIC
        if use_shortener and Config.SHORTENER_API:
            final_link = await get_short_link(link)
        else:
            final_link = link
            
        btn.append([InlineKeyboardButton(f"📁 {file['file_name']}", url=final_link)])

    # Add extra premium ad button if user is free
    if not is_premium:
        btn.append([InlineKeyboardButton("💎 Buy Premium (No Ads)", callback_data="premium_price")])

    await message.reply_text(f"Found {len(files)} results for '{query}':", reply_markup=InlineKeyboardMarkup(btn))
    
