from typing import Any
from database.manager import DbSession
from database.models.user import User
from database.models.pool import Pool, Slot
from datetime import datetime
from sqlmodel import select
from sqlmodel import SQLModel

async def add_to_db(obj: SQLModel) -> Any:
    db = DbSession()
    await db.add_or_update(obj)
    await db.close()
    return obj

async def link_user(discord_id: int, osu_id: int) -> User:
    now = int(datetime.now().timestamp())
    user = User()
    user.discord_id = discord_id
    user.osu_user_id = osu_id
    user.linked_date = now
    return await add_to_db(user)

async def get_linked_user(discord_id: int) -> User | None:
    db = DbSession()
    query = select(User).where(User.discord_id == discord_id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()

async def get_pool_by_name(name: str) -> Pool | None:
    db = DbSession()
    query = select(Pool).where(Pool.name == name)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()

async def get_pool_by_id(id: str) -> Pool | None:
    db = DbSession()
    query = select(Pool).where(Pool.pool_id == id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()

async def get_slot_by_id(id: str) -> Slot | None:
    db = DbSession()
    query = select(Slot).where(Slot.slot_id == id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()

async def is_user_in_party(id: str) -> bool:
    db = DbSession()
    query = select(Slot).where(Slot.slot_id == id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()