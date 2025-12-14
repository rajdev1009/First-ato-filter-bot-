from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

# --- UI & MESSAGES ---

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    # Log to Log Channel
    await client.send_message(Config.LOG_CHANNEL, f"#NEW_USER\nUser: {message.from_user.first_name}\nID: {message.from_user.id}")

    text = "Hi I am a ato filter bot search any movies and series name I find for you"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Premium Price", callback_data="premium_price"),
         InlineKeyboardButton("🎥 Movie Group", url="https://t.me/YOUR_GROUP_LINK")],
        [InlineKeyboardButton("📢 Update Channel", url="https://t.me/YOUR_CHANNEL_LINK"),
         InlineKeyboardButton("⚙ Settings", callback_data="settings")],
        [InlineKeyboardButton("ℹ About", callback_data="about"),
         InlineKeyboardButton("🆘 Help", callback_data="help")]
    ])
    await message.reply_text(text, reply_markup=buttons)

@Client.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    if data == "premium_price":
        # Strictly used figures from request
        prices = (
            "💰 **Premium Plans**\n"
            "Plan A: ₹10\nPlan B: ₹50\nPlan C: ₹90\n"
            "Plan D: ₹1666\nPlan E: ₹73727\n\n"
            "Benefits: No Ads, Direct Links, Priority Support.\n"
            "Contact Admin to buy."
        )
        await callback.message.edit_text(prices)
    
    elif data == "about":
        text = f"**About Bot**\nCreator Name: {Config.CREATOR_NAME}\nFeatures: Auto Filter, Premium, MongoDB"
        await callback.message.edit_text(text)
        
    elif data == "settings" and callback.from_user.id in Config.ADMINS:
        settings = await db.get_settings()
        text = f"**Settings Panel**\nShortener: {settings['shortener']}\nPM Search: {settings['pm_search']}"
        await callback.message.edit_text(text)

# --- ADMIN COMMANDS ---

@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMINS))
async def add_premium_cmd(client, message):
    # Usage: /add_premium user_id days
    try:
        _, user_id, days = message.text.split()
        await db.add_premium(int(user_id), int(days))
        await message.reply_text(f"User {user_id} is now Premium for {days} days.")
        # Premium Log
        await client.send_message(Config.PREMIUM_LOG_CHANNEL, f"#PREMIUM_ADDED\nUser: {user_id}\nDays: {days}")
    except:
        await message.reply_text("Usage: /add_premium user_id days")

@Client.on_message(filters.command("shortener") & filters.user(Config.ADMINS))
async def toggle_shortener(client, message):
    try:
        state = message.text.split()[1].lower() == 'on'
        await db.update_setting('shortener', state)
        await message.reply_text(f"Shortener is now {'ON' if state else 'OFF'}")
    except:
        await message.reply_text("Usage: /shortener on/off")
      
