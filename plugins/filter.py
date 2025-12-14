from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import search_files, count_files, add_user, is_banned
from utils import clean_query, imdb_search
from config import RESULTS_PER_PAGE


@Client.on_message(filters.text)
async def auto_filter(client, message):
    if not message.from_user:
        return

    text = message.text.strip()

    # Ignore commands
    if text.startswith("/"):
        return

    user_id = message.from_user.id
    await add_user(user_id)

    if await is_banned(user_id):
        return

    query = clean_query(text)

    if len(query) < 3:
        return

    total = await count_files(query)
    if total == 0:
        return

    files = await search_files(
        query=query,
        skip=0,
        limit=RESULTS_PER_PAGE
    )

    buttons = []
    for f in files:
        buttons.append([
            InlineKeyboardButton(
                text=f"📁 {f['file_name']}",
                callback_data=f"send|{f['file_id']}"
            )
        ])

    caption = f"🎬 **Results for:** `{query}`\n📁 Found: `{total}`"

    imdb = await imdb_search(query)
    if imdb:
        caption += (
            f"\n\n⭐ IMDB: {imdb.get('rating', 'N/A')}"
            f"\n📝 {imdb.get('plot', '')}"
        )

    await message.reply_text(
        caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )
