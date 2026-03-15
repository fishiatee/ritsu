from database.models.party import Party
from enum import IntEnum
from sqlmodel import SQLModel, Field, Column, JSON

class MatchType(IntEnum):
    DUEL = 0
    OPEN_DUEL = 1
    SOLO = 2

class Participants(SQLModel):
    team_size: int
    red_team: Party
    blue_team: Party

class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    participants: int | Participants = Field(sa_column=Column(JSON))
    type: MatchType
    pool_id: int
    maximum_warmups: int
    best_of: int
    osu_match_id: int
    completed: bool