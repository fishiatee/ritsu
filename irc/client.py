import os
import asyncio
from bottom import Client
from utils import logger

class RitsuIrc:
    __client__: Client
    match_name: str
    match_id: int
    def __init__(self):
        self.match_id = 0
        self.__client__ = Client(host="irc.ppy.sh",
                                 port=6667,
                                 ssl=False)
        self.__client__.on("client_connect")(self.__connect_event__)
        self.__client__.on("privmsg")(self.__priv_msg_event__)
    async def connect(self):
        await self.__client__.connect()
        await self.__client__.wait("CLIENT_DISCONNECT")
        logger.verbose("connection lost with irc, reconnecting...")
        await self.connect()
    async def disconnect(self):
        await self.__client__.disconnect()
        logger.debug("irc client disconnected")
    async def create_match(self):
        await self.__client__.send("privmsg",
                                   target="BanchoBot",
                                   message=f"!mp make {self.match_name}")
    async def __connect_event__(self, **kwargs):
        logger.verbose("authenticating with irc...")
        await self.__client__.send("pass", 
                                   password=os.environ.get("RITSU_OSU_IRC_PASSWORD"))
        await self.__client__.send("nick", 
                                   nick=os.environ.get("RITSU_OSU_IRC_USERNAME"))
        logger.success("connected to irc!")
    async def __priv_msg_event__(self, nick: str, target: str, message: str, **kwargs):
        logger.verbose(f"(irc) PRIVMSG: {nick} -> {target}: {message}")
        if self.match_id == 0 and "https://osu.ppy.sh/mp/" in message and self.match_name in message:
            self.match_id = message.split("https://osu.ppy.sh/mp/", 1)[1].split(" ")[0]
            logger.verbose(f"got match ID: {self.match_id}")
            await self.__client__.send("join",
                                       channel=f"#mp_{self.match_id}")
    @classmethod
    def new(cls, match_name: str):
        client = cls()
        client.match_name = match_name
        asyncio.create_task(client.connect())
        return client