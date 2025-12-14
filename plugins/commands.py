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
    try: await client.send_message(Config.LOG_CHANNEL, f"#NEW_USER: {message.from_user.mention}")
    except: pass
    
    await message.reply_text(
        Script.START_TXT.format(mention=message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Updates", url=Config.UPDATE_CHANNEL_LINK), InlineKeyboardButton("🎥 Group", url=Config.MOVIE_GROUP_LINK)],
            [InlineKeyboardButton("🆘 Help", callback_data="help")]
        ])
    )

@Client.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    
    if data.startswith("file_"):
        try:
            file_id = data.split("_")[1]
            file = await db.get_file(file_id)
            if not file: return await callback.answer("File Not Found", show_alert=True)
            
            await callback.answer("📂 Sending File...", show_alert=False)
            
            caption = (f"🎬 **{file['file_name']}**\n\n"
                       f"⚠️ *Auto Delete in 15 Mins*\n"
                       f"🤖 **Bot:** @{client.me.username}")
            
            btns = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Join Update Channel", url=Config.UPDATE_CHANNEL_LINK)]])
            
            sent = await client.copy_message(
                callback.message.chat.id, Config.DB_CHANNEL, file['file_id'], caption=caption, reply_markup=btns
            )
            
            # Log File Send
            try: await client.send_message(Config.LOG_CHANNEL, f"📤 **File Sent**\n👤: {callback.from_user.mention}\n📂: `{file['file_name']}`")
            except: pass
            
            # Auto Delete (900s = 15 Mins)
            asyncio.create_task(auto_delete(sent, 900))
            
        except Exception as e:
            print(e)
            await callback.answer("Error! Bot needs Admin rights.", show_alert=True)

    elif data == "help":
        await callback.message.edit_text(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    elif data == "start":
        await callback.message.edit_text(Script.START_TXT.format(mention=callback.from_user.mention))
        
