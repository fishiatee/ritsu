from interactions import Member, User

from utils import logger
from utils.misc import gen_hex_str
from database.models.party import Party
from database.managers.party import create_party
from irc.client import RitsuIrc
from enum import StrEnum

class MatchType(StrEnum):
    SOLO = "Solo"
    TEAM = "Team"

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
    __client__: RitsuIrc
    id: str
    type: MatchType
    best_of: int
    pool_id: str
    teams: MatchTeam
    picks: list[MatchPick]
    def __init__(self):
        self.__id__ = gen_hex_str()
    async def start(self):
        pass
    async def initialize(self):
        logger.verbose(f"starting match {self.id}...")
        await self.__client__.create_match()
    @classmethod
    async def create(cls, pool_id: str, best_of: int, dueler: Member | User, opponent: Member | User | None):
        logger.verbose("creating new match...")
        match = cls()
        match.type = MatchType.SOLO
        match.id = gen_hex_str()
        match.best_of = best_of
        match.pool_id = pool_id
        teams = MatchTeam()
        teams.party_1 = await create_party(members=[dueler.id])
        if opponent:
            match.type = MatchType.TEAM
            teams.party_2 = await create_party(members=[opponent.id])
        else:
            teams.party_2 = await create_party(name="Solo Match")
        match.teams = teams
        logger.verbose("initializing new irc client...")
        match_name = f"RITSU: ({match.teams.party_1.name}) vs ({match.teams.party_2.name})"
        match.__client__ = RitsuIrc.new(match_name)
        logger.success(f"created new match {match.id}!")
        return match