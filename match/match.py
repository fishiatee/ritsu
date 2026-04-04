from utils import logger
from utils.misc import gen_hex_str
from database.models.party import Party
from database.managers.party import create_party
from irc import IrcClient
from dataclasses import dataclass
from enum import IntEnum

class MatchType(IntEnum):
    SOLO = 0
    TEAM = 1

class MatchTeam:
    party_1: Party
    party_2: Party | None
    __points__: list[int] = [0, 0]
    def get_team_1_points(self) -> int:
        return self.__points__[0]
    def get_team_2_points(self) -> int:
        return self.__points__[1]
    def set_team_1_points(self, points: int):
        self.__points__[0] = points
    def set_team_2_points(self, points: int):
        self.__points__[1] = points

class MatchPick:
    name: str
    slot_id: str
    party: Party

class Match:
    __client__: IrcClient
    id: str
    type: MatchType
    best_of: int
    pool_id: str
    teams: MatchTeam
    picks: list[MatchPick]
    def __init__(self):
        self.__id__ = gen_hex_str()
        self.__client__ = IrcClient(self)
    async def start(self):
        pass
    @classmethod
    async def create(cls, pool_id: str, best_of: int, dueler_id: int, opponent_id: int | None):
        logger.verbose("creating new match...")
        match = cls()
        match.type = MatchType.SOLO
        match.id = gen_hex_str()
        match.best_of = best_of
        match.pool_id = pool_id
        teams = MatchTeam()
        teams.party_1 = await create_party([dueler_id])
        if opponent_id:
            match.type = MatchType.TEAM
            teams.party_2 = await create_party([opponent_id])
        match.teams = teams
        logger.verbose("initializing new irc client...")
        return match