from sqlmodel import SQLModel, Field, Column, JSON

class Freemod(SQLModel):
    allowed_mods: list[str]
    nm_multiplier: float
    hr_multiplier: float
    hd_multiplier: float
    ez_multiplier: float
    fl_multiplier: float

class Slot(SQLModel):
    name: str
    pooler_note: str
    freemod: Freemod
    tiebreaker: bool
    mods: list[str]
    map_id: int

class Pool(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    poolers: list[str] = Field(sa_column=Column(JSON))
    description: str
    creator_id: int
    creation_date: int
    slots: list[Slot] = Field(sa_column=Column(JSON))