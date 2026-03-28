from sqlmodel import SQLModel, Field, Column, JSON

class Match(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    match_id: str
    type: int
    room_id: int
    pool_id: int
    parties: list[str] = Field(sa_column=Column(JSON))
    points: list[int] = Field(sa_column=Column(JSON))
    best_of: int