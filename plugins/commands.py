from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", url=Config.UPDATE_CHANNEL_LINK),
         InlineKeyboardButton("🎥 Group", url=Config.MOVIE_GROUP_LINK)],
        [InlineKeyboardButton("🆘 Help", callback_data="help"),
         InlineKeyboardButton("⚡ Developer", url=f"https://t.me/{Config.ADMIN_USERNAME}")]
    ])
    await message.reply("👋 Welcome! Search movies & series.", reply_markup=buttons)

@Client.on_message(filters.command("help") & filters.private)
async def help_msg(client, message):
    await message.reply("ℹ️ Type movie name to search.\n💎 Buy premium for extra features.")
    
