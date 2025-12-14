from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
from script import Script

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    try:
        await client.send_message(Config.LOG_CHANNEL, f"#NEW_USER\nUser: {message.from_user.first_name}\nID: {message.from_user.id}")
    except: pass

    text = Script.START_TXT.format(mention=message.from_user.mention)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Premium Price", callback_data="premium_price"),
         InlineKeyboardButton("🎥 Movie Group", url="https://t.me/+mgQzW_pjxT1hODI1")],
        [InlineKeyboardButton("📢 Update Channel", url="https://t.me/+YZ7qQ1Ahx-M1MDdl"),
         InlineKeyboardButton("⚙ Settings", callback_data="settings")],
        [InlineKeyboardButton("ℹ About", callback_data="about"),
         InlineKeyboardButton("🆘 Help", callback_data="help")]
    ])
    await message.reply_text(text, reply_markup=buttons)

@Client.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    if data == "premium_price":
        await callback.message.edit_text(Script.PREMIUM_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif data == "about":
        await callback.message.edit_text(Script.ABOUT_TXT.format(creator=Config.CREATOR_NAME), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif data == "help":
        await callback.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif data == "settings" and callback.from_user.id in Config.ADMINS:
        s = await db.get_settings()
        await callback.message.edit_text(f"Shortener: {s['shortener']}\nPM Search: {s['pm_search']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif data == "start":
        await callback.message.edit_text(Script.START_TXT.format(mention=callback.from_user.mention), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Premium Price", callback_data="premium_price"),
         InlineKeyboardButton("🎥 Movie Group", url="https://t.me/Raj_Hd_movies")],
        [InlineKeyboardButton("📢 Update Channel", url="https://t.me/YOUR_CHANNEL_LINK"),
         InlineKeyboardButton("⚙ Settings", callback_data="settings")],
        [InlineKeyboardButton("ℹ About", callback_data="about"),
         InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]))
        
