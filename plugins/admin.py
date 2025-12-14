import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid

from database import (
    add_file,
    ban_user,
    unban_user,
    get_stats,
    set_shortener
)
from config import ADMINS


# ───────────── ADMIN FILTER ─────────────
def admin_only(_, __, message):
    return message.from_user and message.from_user.id in ADMINS


admin_filter = filters.create(admin_only)


# ───────────── INDEX COMMAND ─────────────
@Client.on_message(filters.command("index") & admin_filter)
async def index_files(client, message):
    if len(message.command) != 2:
        return await message.reply_text("❌ Usage:\n`/index channel_username_or_id`")

    channel = message.command[1]
    msg = await message.reply_text("🔍 Indexing started...")

    indexed = 0

    try:
        async for m in client.get_messages(channel, limit=100000):
            if not m.document and not m.video:
                continue

            file = m.document or m.video

            file_data = {
                "file_id": file.file_id,
                "file_name": file.file_name or "No Name",
                "file_size": file.file_size,
                "chat_id": m.chat.id,
                "message_id": m.id
            }

            await add_file(file_data)
            indexed += 1

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except PeerIdInvalid:
        return await msg.edit("❌ Invalid channel / bot not added")

    await msg.edit(f"✅ Indexing completed\n📁 Files indexed: `{indexed}`")


# ───────────── STATS ─────────────
@Client.on_message(filters.command("stats") & admin_filter)
async def stats_cmd(client, message):
    stats = await get_stats()

    await message.reply_text(
        "📊 **Bot Stats**\n\n"
        f"👥 Users: `{stats['users']}`\n"
        f"📁 Files: `{stats['files']}`"
    )


# ───────────── BAN USER ─────────────
@Client.on_message(filters.command("ban") & admin_filter)
async def ban_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to user message")

    user_id = message.reply_to_message.from_user.id
    await ban_user(user_id)
    await message.reply_text("🚫 User banned")


# ───────────── UNBAN USER ─────────────
@Client.on_message(filters.command("unban") & admin_filter)
async def unban_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to user message")

    user_id = message.reply_to_message.from_user.id
    await unban_user(user_id)
    await message.reply_text("✅ User unbanned")


# ───────────── SHORTENER ON/OFF ─────────────
@Client.on_message(filters.command("shortener") & admin_filter)
async def shortener_cmd(client, message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: `/shortener on|off`")

    value = message.command[1].lower()

    if value == "on":
        await set_shortener(True)
        await message.reply_text("🔗 Shortener ENABLED")
    elif value == "off":
        await set_shortener(False)
        await message.reply_text("🔗 Shortener DISABLED")
    else:
        await message.reply_text("Use on / off")


# ───────────── BROADCAST ─────────────
@Client.on_message(filters.command("broadcast") & admin_filter)
async def broadcast_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to message to broadcast")

    from database import users_col

    sent = 0
    async for user in users_col.find({}):
        try:
            await message.reply_to_message.copy(user["_id"])
            sent += 1
            await asyncio.sleep(0.05)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

    await message.reply_text(f"📣 Broadcast sent to `{sent}` users")
