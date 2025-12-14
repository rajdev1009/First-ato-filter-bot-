import os
import asyncio
from pyrogram import Client, idle
from aiohttp import web
from config import Config

# --- Fake Web Server for Koyeb/Render ---
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "running", "message": "Raj HD Movies Bot is Alive!"})

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

    async def stop(self, *args):
        await super().stop()
        print("❌ Bot Stopped")

async def main():
    # Initialize Bot
    bot = Bot()

    # Create Web Server
    app = web.AppRunner(await web_server())
    await app.setup()
    
    # Bind to Port provided by Koyeb (or default 8080)
    bind_address = "0.0.0.0"
    port = int(os.environ.get("PORT", 8080))
    
    await web.TCPSite(app, bind_address, port).start()
    print(f"🌍 Web Server Started on Port {port}")

    # Start Bot
    await bot.start()
    await idle()
    await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
