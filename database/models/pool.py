from sqlmodel import SQLModel, Field, Column, JSON

class Slot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slot_id: str
    pooler_note: str = Field(default="")
    force_mod: bool = Field(default=False)
    tiebreaker: bool = Field(default=False)
    mods: list[str] = Field(sa_column=Column(JSON))
    map_id: int

class Pool(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    pool_id: str
    game_mode: str
    description: str = Field(default="")
    creator_id: int
    creation_date: int
    slots: dict[str, str] = Field(sa_column=Column(JSON))