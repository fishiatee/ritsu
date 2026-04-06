from datetime import datetime
from sqlmodel import select
from cashews import cache
from database.manager import DbSession
from database.models.user import User

@cache(ttl="2m")
async def get_linked_user(discord_id: int) -> User | None:
    db = DbSession()
    query = select(User).where(User.discord_id == discord_id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()

async def link_user(discord_id: int, osu_id: int):
    now = int(datetime.now().timestamp())
    user = User()
    user.discord_id = discord_id
    user.osu_user_id = osu_id
    user.linked_date = now
    await DbSession.add_to_db(user)