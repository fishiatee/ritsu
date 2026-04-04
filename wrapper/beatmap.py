from wrapper.manager import get_client
from utils import logger
from cashews import cache
from osu import Beatmap, BeatmapDifficultyAttributes
from osu.exceptions import RequestException

@cache(ttl="1h")
async def get_beatmap_data(id: int) -> Beatmap | None:
    logger.verbose(f"(wrapper/beatmap) get_beatmap_data() called with id {id}")
    client = get_client()
    try:
        r = await client.get_beatmap(id)
    except RequestException:
        return None
    return r

async def get_beatmap_attr_data(id: int, mods: list[str]) -> BeatmapDifficultyAttributes | None:
    logger.verbose(f"(wrapper/beatmap) get_beatmap_attr_data() called with id {id} and mods {mods}")
    client = get_client()
    if "NF" in mods:
        mods.pop(mods.index("NF"))
    try:
        if len(mods) > 0:
            r = await client.get_beatmap_attributes(beatmap=id,
                                                    mods=mods)
        else:
            r = await client.get_beatmap_attributes(beatmap=id)
    except RequestException:
        return None
    return r