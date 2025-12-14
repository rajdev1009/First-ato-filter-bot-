import os
import asyncio
from pyrogram import Client, idle
from aiohttp import web
from config import Config

routes = web.RouteTableDef()
@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "running"})

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

class Bot(Client):
    def __init__(self):
        super().__init__("ProBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, plugins=dict(root="plugins"))

    async def start(self):
        await super().start()
        print("✅ Raj HD Movies Bot Started!")
        
        # 🔥 PERMANENT FIX FOR PEER ID INVALID 🔥
        try:
            print("🔄 Refreshing Channel Cache...")
            # Hum zabardasti DB Channel ka data mangenge taaki cache ban jaye
            await self.get_chat(Config.DB_CHANNEL)
            print("✅ DB Channel Connected Successfully!")
        except Exception as e:
            print(f"❌ Failed to connect to DB Channel: {e}")
            print("⚠️ Make sure Bot is Admin in DB Channel!")

    async def stop(self, *args):
        await super().stop()

async def main():
    bot = Bot()
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", int(os.environ.get("PORT", 8080))).start()
    await bot.start()
    await idle()
    await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
