from wrapper.manager import get_client
from cashews import cache
from osu import GameModeStr, UserCompact, User

@cache(ttl="1h")
async def search_osu_profiles(name: str, limit: int = 1) -> UserCompact | None:
    client = get_client()
    r = await client.search(mode="user",
                            query=name)
    if r.user and len(r.user) <= limit:
        return r.user[limit - 1]
    else:
        return None
    
@cache(ttl="1h")
async def get_user_profile(id: str, mode: GameModeStr = GameModeStr.STANDARD) -> User | None:
    client = get_client()
    return await client.get_user(id,
                                 mode=mode)