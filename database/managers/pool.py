from cashews import cache
from sqlmodel import select
from database.manager import DbSession
from database.models.pool import Pool, Slot

@cache(ttl="2h")
async def get_pool(id: str) -> Pool | None:
    db = DbSession()
    query = select(Pool).where(Pool.pool_id == id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()

@cache(ttl="2h")
async def get_slot(id: str) -> Slot | None:
    db = DbSession()
    query = select(Slot).where(Slot.slot_id == id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()