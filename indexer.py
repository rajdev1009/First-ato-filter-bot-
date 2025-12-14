import asyncio
from pyrogram import Client
from database import db
from config import Config

SESSION_STRING = "YOUR_USER_SESSION_STRING_HERE"

async def main():
    async with Client(
        "user_indexer",
        session_string=SESSION_STRING,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH
    ) as client:
        print("✅ User account connected")
        async for message in client.get_chat_history(Config.DB_CHANNEL, limit=0):
            try:
                if message.document or message.video:
                    saved = await db.save_file(message)
                    if saved:
                        print(f"📥 Saved: {message.id} / {message.caption or 'No Caption'}")
            except Exception as e:
                print(f"⚠️ Error saving message {message.id}: {e}")
            await asyncio.sleep(0.2)
        print("✅ Indexing complete!")

if __name__ == "__main__":
    asyncio.run(main())
  
