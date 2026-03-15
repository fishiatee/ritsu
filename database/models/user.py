from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    osu_user_id: int
    discord_id: int
    linked_date: int