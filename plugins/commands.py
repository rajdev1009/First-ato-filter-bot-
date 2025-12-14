from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
from script import Script

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    try:
        await client.send_message(Config.LOG_CHANNEL, f"#NEW_USER\nUser: {message.from_user.mention}")
    except: pass

    text = Script.START_TXT.format(mention=message.from_user.mention)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Premium Price", callback_data="premium_price"),
         InlineKeyboardButton("🎥 Movie Group", url="https://t.me/Raj_Hd_movies")],
        [InlineKeyboardButton("⚙ Settings", callback_data="settings"),
         InlineKeyboardButton("🆘 Help", callback_data="help")]
    ])
    await message.reply_text(text, reply_markup=buttons)

@Client.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    if data == "premium_price":
        # CONTACT ADMIN BUTTON ADDED
        btn = [[InlineKeyboardButton("👤 Contact Admin", url="https://t.me/YOUR_USERNAME"), InlineKeyboardButton("🔙 Back", callback_data="start")]]
        await callback.message.edit_text(Script.PREMIUM_TXT, reply_markup=InlineKeyboardMarkup(btn))
    elif data == "help":
        await callback.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif data == "start":
        await callback.message.edit_text(Script.START_TXT.format(mention=callback.from_user.mention))
        
