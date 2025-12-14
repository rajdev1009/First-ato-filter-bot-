from pyrogram import Client, filters
from database import add_user, is_banned


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id

    await add_user(user_id)

    if await is_banned(user_id):
        return

    await message.reply_text(
        "👋 **Welcome to Advanced Auto Filter Bot**\n\n"
        "🎬 बस movie / series का नाम भेजो\n"
        "📁 File buttons के साथ मिल जाएगी\n\n"
        "💡 Example:\n`Pushpa`\n`KGF 2`"
    )


@Client.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text(
        "📌 **How to Use**\n\n"
        "1️⃣ Movie का नाम लिखो\n"
        "2️⃣ Buttons से file चुनो\n"
        "3️⃣ File auto-delete हो जाएगी\n\n"
        "🛠 **Admin Commands**\n"
        "/index\n"
        "/stats\n"
        "/broadcast\n"
        "/ban / unban"
    )
