from utils.db import get_slot_by_id
from database.models.pool import Slot
from wrapper.beatmap import get_beatmap_attr_data
from cashews import cache

@cache(ttl="24h")
async def calculate_sr(slot: Slot) -> float:
    mods = slot.mods
    if len(mods) > 0 and "NF" in mods:
        mods.pop(mods.index("NF"))
    if slot.tiebreaker or slot.force_mod:
        mods = []
    data = await get_beatmap_attr_data(slot.map_id, mods)
    return data.star_rating

@cache(ttl="24h")
async def calculate_avg_sr(slot_ids: list[str]) -> float:
    srs = 0
    avg_sr = 0
    for id in slot_ids:
        slot = await get_slot_by_id(id)
        avg_sr += await calculate_sr(slot)
        srs += 1
    avg_sr = avg_sr / srs
    return avg_sr