import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from database import init_db

# ───────────── LOGGING ─────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# ───────────── PYROGRAM CLIENT ─────────────
app = Client(
    name="AutoFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)


# ───────────── ON START ─────────────
@app.on_startup
async def start_bot(client):
    await init_db()
    print("✅ Bot started & Database initialized")


# ───────────── RUN ─────────────
if __name__ == "__main__":
    app.run()
