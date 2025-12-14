import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from database import (
    get_file,
    search_files,
    count_files
)
from config import RESULTS_PER_PAGE, AUTO_DELETE_TIME
from utils import clean_query


# ───────────── CALLBACK HANDLER ─────────────
@Client.on_callback_query(filters.regex("^(send|page)"))
async def callback_handler(client, query):
    data = query.data.split("|")
    action = data[0]

    try:
        # ───────────── SEND FILE ─────────────
        if action == "send":
            file_id = data[1]
            file = await get_file(file_id)

            if not file:
                return await query.answer("❌ File not found", show_alert=True)

            msg = await client.copy_message(
                chat_id=query.from_user.id,
                from_chat_id=file["chat_id"],
                message_id=file["message_id"]
            )

            await query.answer("📥 File sent!")

            # auto delete
            await asyncio.sleep(AUTO_DELETE_TIME)
            await msg.delete()

        # ───────────── PAGINATION ─────────────
        elif action == "page":
            query_text = clean_query(data[1])
            page = int(data[2])

            total = await count_files(query_text)
            files = await search_files(
                query=query_text,
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

            nav_buttons = []

            if page > 0:
                nav_buttons.append(
                    InlineKeyboardButton(
                        "⬅️ Back",
                        callback_data=f"page|{query_text}|{page - 1}"
                    )
                )

            if (page + 1) * RESULTS_PER_PAGE < total:
                nav_buttons.append(
                    InlineKeyboardButton(
                        "Next ➡️",
                        callback_data=f"page|{query_text}|{page + 1}"
                    )
                )

            if nav_buttons:
                buttons.append(nav_buttons)

            await query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(buttons)
            )

            await query.answer()

    except FloodWait as e:
        await asyncio.sleep(e.value)
