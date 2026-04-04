import os
import asyncio
from utils import logger
from database.manager import DbSession
from irc import IrcManager
from dotenv import load_dotenv
from cashews import cache
from interactions import Client, Intents, listen

bot = Client(intents=Intents.DEFAULT,
             send_command_tracebacks=False)

@listen()
async def on_ready():
    logger.success("ritsu is ready!")

async def async_init():
    await DbSession.initialize_db()

if __name__ == "__main__":
    logger.info("initializing ritsu...")
    load_dotenv()
    cache.setup("mem://")
    asyncio.run(async_init())
    IrcManager.initialize_irc()
    bot.load_extension("extensions.discord")
    bot.load_extension("extensions.pool")
    bot.load_extension("extensions.duel")
    bot.start(os.environ.get("RITSU_DISCORD_BOT_TOKEN"))