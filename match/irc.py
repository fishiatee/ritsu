from match.match import Match
from pydle import Client

class IrcClient(Client):
    match: Match
    def __init__(self, match: Match):
        self.match = match
    async def on_connect(self):
        await self.message("BanchoBot", "!help")