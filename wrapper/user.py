from wrapper.manager import get_client
from cashews import cache
from osu import UserCompact

@cache(ttl="1h")
async def search_osu_profiles(name: str, limit: int = 1) -> UserCompact | None:
    client = get_client()
    r = await client.search(mode="user",
                            query=name)
    if r.user and len(r.user) <= limit:
        return r.user[limit - 1]
    else:
        return None