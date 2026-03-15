from database.manager import DbSession
from database.models.user import User
from datetime import datetime
from sqlmodel import select

async def link_user(discord_id: int, osu_id: int) -> User:
    now = int(datetime.now().timestamp())
    db = DbSession()
    user = User()
    user.discord_id = discord_id
    user.osu_user_id = osu_id
    user.linked_date = now
    await db.add_or_update(user)
    await db.close()
    return user

async def get_linked_user(discord_id: int) -> User | None:
    db = DbSession()
    query = select(User).where(User.discord_id == discord_id)
    r = await db.execute_sql(query)
    await db.close()
    return r.one_or_none()