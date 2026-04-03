from utils import logger
from utils.misc import gen_hex_str
from database.models.party import Party
from match.irc import IrcClient
from dataclasses import dataclass
from enum import IntEnum

class MatchType(IntEnum):
    SOLO = 0
    TEAM = 1

@dataclass(init=False)
class MatchTeam:
    party_1: Party
    party_2: Party | None
    points: list[int]

@dataclass(init=False)
class MatchPick:
    name: str
    slot_id: str
    party: Party

class Match:
    __client__: IrcClient
    id: str
    type: MatchType
    best_of: int
    teams: MatchTeam
    picks: list[MatchPick]
    def __init__(self):
        self.id = gen_hex_str()
        self.properties = MatchProperties()
        self.__client__ = IrcClient(self)
    async def start(self):
        await self.__client__.connect(hostname="irc.ppy.sh",
                                      port=6667,
                                      reconnect=True)