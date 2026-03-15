import os
import asyncio
from utils.logger import Logger
from database.manager import create_db
from dotenv import load_dotenv
from cashews import cache
from interactions import Client, Intents, listen

bot = Client(intents=Intents.DEFAULT,
             send_command_tracebacks=False)

@listen()
async def on_ready():
    Logger.success("ritsu is ready!")

def init():
    load_dotenv()
    cache.setup("mem://")
    asyncio.run(create_db())
    bot.load_extension("extensions.discord")
    bot.start(os.environ.get("RITSU_DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    Logger.info("initializing ritsu...")
    init()