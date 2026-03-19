from utils.misc import gen_hex_str
from utils.db import add_to_db
from database.models.pool import Pool, Slot
from datetime import datetime

async def build_pool(manifest: dict, creator_id: int) -> str:
    pool = Pool()
    pool_id  = gen_hex_str()
    pool.name = manifest["name"]
    pool.pool_id = pool_id
    pool.game_mode = manifest["game_mode"]
    pool.slots = {}
    pool.creation_date = int(datetime.now().timestamp())
    pool.creator_id = creator_id
    if "description" in manifest.keys():
        pool.description = manifest["description"]
    for i in manifest["slots"]:
        slot_id = gen_hex_str()
        slot = Slot(slot_id=slot_id,
                    mods=i["mods"],
                    map_id=i["map_id"])
        if "note" in i.keys():
            slot.pooler_note = i["note"]
        if "force_mod" in i.keys():
            slot.force_mod = i["force_mod"]
        if "tiebreaker" in i.keys():
            slot.tiebreaker = i["tiebreaker"]
        pool.slots[i["name"]] = slot_id
        await add_to_db(slot)
    await add_to_db(pool)
    return pool_id