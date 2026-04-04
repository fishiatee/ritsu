import os
import asyncio
from pydle import Client
from utils import logger

client: Client

class IrcClient(Client):
    async def on_connect(self):
        await super().on_connect()
        logger.success("irc client connected!")
        await self.message("BanchoBot", "!help")
    async def on_raw_311(self, msg):
        # Prevent ValueError spamming
        pass
    
class IrcManager:
    @staticmethod
    def initialize_irc():
        global client
        logger.info("initializing irc client...")
        client = IrcClient(os.environ.get("RITSU_OSU_IRC_USERNAME"))
        asyncio.run(client.connect(hostname="irc.ppy.sh",
                             port=6667,
                             password=os.environ.get("RITSU_OSU_IRC_PASSWORD")))
        client.handle_forever()
    def get_client() -> IrcClient:
        global client
        return client