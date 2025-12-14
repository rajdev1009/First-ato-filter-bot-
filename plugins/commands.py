import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
from script import Script

async def auto_delete(msg, delay):
    await asyncio.sleep(delay)
    try: await msg.delete()
    except: pass

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", url=Config.UPDATE_CHANNEL_LINK), 
         InlineKeyboardButton("🎥 Group", url=Config.MOVIE_GROUP_LINK)],
        [InlineKeyboardButton("🆘 Help", callback_data="help"),
         InlineKeyboardButton("⚡ Developer", url="https://t.me/Raj_Hd_movies")]
    ])
    await message.reply_text(Script.START_TXT.format(mention=message.from_user.mention), reply_markup=buttons)

@Client.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    
    if data.startswith("file_"):
        try:
            file_id = data.split("_")[1]
            file = await db.get_file(file_id)
            if not file: return await callback.answer("❌ File Not Found", show_alert=True)

            await callback.answer("📂 Sending File...", show_alert=False)
            
            caption = (f"🎬 **{file['file_name']}**\n\n⚠️ *Auto Delete in 15 Mins*\n⚡ Powered by Raj Dev")
            btns = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Join Update Channel", url=Config.UPDATE_CHANNEL_LINK)]])
            
            sent = await client.copy_message(
                chat_id=callback.message.chat.id,
                from_chat_id=Config.DB_CHANNEL,
                message_id=file['file_id'],
                caption=caption,
                reply_markup=btns
            )
            asyncio.create_task(auto_delete(sent, 900))
        except Exception as e:
            print(f"Send Error: {e}")
            await callback.answer(f"⚠️ Error: {e}", show_alert=True)

    elif data == "premium_price":
        url = f"https://t.me/{Config.ADMIN_USERNAME}"
        btn = [[InlineKeyboardButton("👤 Contact Admin", url=url)], [InlineKeyboardButton("🔙 Back", callback_data="start")]]
        await callback.message.edit_text(Script.PREMIUM_TXT, reply_markup=InlineKeyboardMarkup(btn))
    elif data == "help":
        await callback.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "start":
        await callback.message.edit_text(Script.START_TXT.format(mention=callback.from_user.mention))
        
