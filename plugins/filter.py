from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

@Client.on_message(filters.chat(Config.DB_CHANNEL) & (filters.document | filters.video))
async def auto_save(client, message):
    await db.save_file(message)

@Client.on_message(filters.text & filters.private)
async def auto_filter(client, message):
    if message.text.startswith("/"):
        return

    files = await db.search_files(message.text)
    if not files:
        return await message.reply("No results found.")

    btn = []
    for file in files:
        # 👇 यहाँ जादू है: URL हटा दिया, अब यह सीधा फाइल मांगेगा
        # हम फाइल का MongoDB ID बटन में छिपा रहे हैं
        btn.append([InlineKeyboardButton(f"📁 {file['file_name']}", callback_data=f"file_{file['_id']}")])

    # Premium बटन (Optional)
    is_premium = await db.is_user_premium(message.from_user.id)
    if not is_premium:
        btn.append([InlineKeyboardButton("💎 Buy Premium (Fast Speed)", callback_data="premium_price")])

    await message.reply_text(f"Found {len(files)} results:", reply_markup=InlineKeyboardMarkup(btn))
    
