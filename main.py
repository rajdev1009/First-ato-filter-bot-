import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from database import init_db

logging.basicConfig(level=logging.INFO)

app = Client(
    "AutoFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():
    async with app:
        await init_db()
        print("✅ Raj HD Movies Bot Started!")
        await asyncio.Event().wait()  # keep bot alive

if __name__ == "__main__":
    asyncio.run(main())
