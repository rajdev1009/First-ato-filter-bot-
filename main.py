from pyrogram import Client
from config import Config

class Bot(Client):
    def __init__(self):
        super().__init__(
            "AutoFilterBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("Bot Started! Created for Raj HD Movies")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped")

app = Bot()
app.run()
