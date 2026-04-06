from sqlmodel import SQLModel, Field, Column, JSON

class Party(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    leader_id: str
    members: list[int] = Field(sa_column=Column(JSON))