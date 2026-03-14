import os
from utils.logger import Logger
from dotenv import load_dotenv
from interactions import Client, Intents, listen

bot = Client(intents=Intents.DEFAULT,
             send_command_tracebacks=False,
             auto_defer=True,
             status="Playing osu!")

@listen()
async def on_ready():
    Logger.success("ritsu is ready!")

def init():
    bot.start(os.environ.get("RITSU_DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    Logger.info("initializing ritsu...")
    load_dotenv()
    init()