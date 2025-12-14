from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
from script import Script

# --- START COMMAND ---
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # 1. Add User to Database
    await db.add_user(message.from_user.id, message.from_user.first_name)
    
    # 2. Send Notification to Log Channel
    try:
        await client.send_message(
            Config.LOG_CHANNEL, 
            f"#NEW_USER\nUser: {message.from_user.first_name}\nID: {message.from_user.id}\nMention: {message.from_user.mention}"
        )
    except:
        pass

    # 3. Send Welcome Message
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

# --- CALLBACK HANDLER (BUTTONS) ---
@Client.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    
    if data == "premium_price":
        # 🟢 EDIT THIS: अपना टेलीग्राम यूजरनेम यहाँ लिखें (Quotes के अंदर)
        admin_username = "raj_dev_01" 
        
        btn = [
            [InlineKeyboardButton("👤 Contact Admin / Send Proof", url=f"https://t.me/{admin_username}")],
            [InlineKeyboardButton("🔙 Back", callback_data="start")]
        ]
        await callback.message.edit_text(Script.PREMIUM_TXT, reply_markup=InlineKeyboardMarkup(btn))
    
    elif data == "about":
        btn = [[InlineKeyboardButton("🔙 Back", callback_data="start")]]
        await callback.message.edit_text(
            Script.ABOUT_TXT.format(creator=Config.CREATOR_NAME), 
            reply_markup=InlineKeyboardMarkup(btn)
        )
        
    elif data == "help":
        btn = [[InlineKeyboardButton("🔙 Back", callback_data="start")]]
        await callback.message.edit_text(
            Script.HELP_TXT, 
            reply_markup=InlineKeyboardMarkup(btn)
        )
        
    elif data == "settings":
        # Only Admin can see settings
        if callback.from_user.id in Config.ADMINS:
            settings = await db.get_settings()
            status_text = f"**⚙ Settings Panel**\n\n🔹 Shortener: `{settings['shortener']}`\n🔹 PM Search: `{settings['pm_search']}`"
            btn = [[InlineKeyboardButton("🔙 Back", callback_data="start")]]
            await callback.message.edit_text(status_text, reply_markup=InlineKeyboardMarkup(btn))
        else:
            await callback.answer("Only Admins can use this!", show_alert=True)
            
    elif data == "start":
        # Back to Main Menu
        text = Script.START_TXT.format(mention=callback.from_user.mention)
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔥 Premium Price", callback_data="premium_price"),
             InlineKeyboardButton("🎥 Movie Group", url="https://t.me/+u4cmm3JmIrFlNzZl")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/+YZ7qQ1Ahx-M1MDdl"),
             InlineKeyboardButton("⚙ Settings", callback_data="settings")],
            [InlineKeyboardButton("ℹ About", callback_data="about"),
             InlineKeyboardButton("🆘 Help", callback_data="help")]
        ])
        await callback.message.edit_text(text, reply_markup=buttons)
        
