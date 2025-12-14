from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import (
    search_files,
    count_files,
    add_user,
    is_banned
)
from utils import clean_query, imdb_search
from config import RESULTS_PER_PAGE


@Client.on_message(filters.text & ~filters.edited)
async def auto_filter(client, message):

    if not message.from_user:
        return

    text = message.text.strip()

    # ✅ Ignore commands SAFELY
    if text.startswith("/"):
        return

    user_id = message.from_user.id
    await add_user(user_id)

    # ban check
    if await is_banned(user_id):
        return

    # clean movie name
    query = clean_query(text)

    # ignore very small queries
    if len(query) < 3:
        return

    total = await count_files(query)
    if total == 0:
        return

    page = 0
    files = await search_files(
        query=query,
        skip=page * RESULTS_PER_PAGE,
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

    # pagination
    if total > RESULTS_PER_PAGE:
        buttons.append([
            InlineKeyboardButton(
                "Next ➡️",
                callback_data=f"page|{query}|1"
            )
        ])

    # imdb info
    imdb = await imdb_search(query)

    caption = f"🎬 **Results for:** `{query}`\n📁 Found: `{total}`"
    if imdb:
        caption += (
            f"\n\n⭐ **IMDB:** {imdb.get('rating', 'N/A')}"
            f"\n📝 {imdb.get('plot', 'Not Available')}"
        )

    # send result
    if imdb and imdb.get("poster") and imdb["poster"] != "N/A":
        await message.reply_photo(
            photo=imdb["poster"],
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
