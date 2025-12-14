from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
from script import Script

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
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
    
    # 👇👇👇 FILE SENDING LOGIC (Ye Naya Hai) 👇👇👇
    if data.startswith("file_"):
        try:
            file_mongo_id = data.split("_")[1]
            file_info = await db.get_file(file_mongo_id)
            
            if not file_info:
                return await callback.answer("File not found!", show_alert=True)

            # Check Premium for Shortener (Optional Logic here)
            # अभी हम सीधा फाइल भेज रहे हैं जैसा आपने मांगा
            
            await callback.answer("📂 Sending File...", show_alert=False)
            
            # DB Channel se User ko file Copy karein
            await client.copy_message(
                chat_id=callback.from_user.id,
                from_chat_id=Config.DB_CHANNEL,
                message_id=file_info['file_id'],
                caption=f"🎥 **{file_info['file_name']}**\n\n✅ Join: @Raj_Hd_movies"
            )
        except Exception as e:
            print(f"Send Error: {e}")
            await callback.answer("Error sending file. Make sure Bot is Admin in DB Channel.", show_alert=True)
            
    # --- Other Buttons ---
    elif data == "premium_price":
        # CONTACT ADMIN BUTTON
        btn = [[InlineKeyboardButton("👤 Contact Admin", url="https://t.me/YOUR_USERNAME"), InlineKeyboardButton("🔙 Back", callback_data="start")]]
        await callback.message.edit_text(Script.PREMIUM_TXT, reply_markup=InlineKeyboardMarkup(btn))
    elif data == "help":
        await callback.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
    elif data == "start":
        await callback.message.edit_text(Script.START_TXT.format(mention=callback.from_user.mention))
        
