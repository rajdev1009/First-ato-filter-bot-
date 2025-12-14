import os
import asyncio
from pyrogram import Client, idle
from aiohttp import web
from config import Config

# --- Web Server for Koyeb ---
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "running", "message": "Bot is Alive!"})

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

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
        print("✅ Bot Started! Created for Raj HD Movies")
        
        # Notification to Log Channel
        try:
            await self.send_message(
                Config.LOG_CHANNEL, 
                "🟢 **Bot Is Live!**\n\nI have successfully restarted and I am online now. 🚀"
            )
        except Exception as e:
            print(f"Log Error: {e}")

    async def stop(self, *args):
        await super().stop()
        print("❌ Bot Stopped")

async def main():
    bot = Bot()
    app = web.AppRunner(await web_server())
    await app.setup()
    
    bind_address = "0.0.0.0"
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(app, bind_address, port).start()
    
    await bot.start()
    await idle()
    await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
