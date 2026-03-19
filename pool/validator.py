from utils.logger import Logger
from wrapper.beatmap import get_beatmap_data
from typing import Any

# this is prolly overkill
# but for a public-facing bot, i think its helpful???
async def validate_pool(manifest: Any) -> list[str]:
    # check if its a valid dict to begin with
    if not type(manifest) is dict:
        return ["- not a YAML file"]
    Logger.info("validating pool manifest...")
    issues = []
    unique_map_ids = {}
    # ensure required fields
    if not "name" in manifest.keys():
        issues.append("- the pool must be given a name (`name` property)")
    if not "game_mode" in manifest.keys():
        issues.append("- the game mode of the pool must be set (`game_mode` property)")
    if not "slots" in manifest.keys():
        issues.append("- the pool must have maps (`slots` property)")
    # ensure correct datatype
    if not type(manifest["name"]) is str:
        issues.append("- `name` property is not a valid name")
    if "description" in manifest.keys() and not type(manifest["description"]) is str:
        issues.append("- `description` property is not a valid description")
    if not type(manifest["slots"]) is list:
        issues.append("- `slots` property is not a list of maps")
    # ensure gamemode is valid
    if not manifest["game_mode"].lower() in ["osu", "mania", "taiko", "catch"]:
        issues.append("- `game_mode` property is not a valid game mode (`osu`, `mania`, `taiko` or `catch`)")
    # ensure there's atleast 1 slot
    if len(manifest["slots"]) < 1:
        issues.append("- there MUST be at least 1 map in the pool")
    # slot checking
    for slot in manifest["slots"]:
        # ensure slot is dict
        if not type(slot) is dict:
            issues.append(f"- no valid definition exist for slot index {manifest["slots"].index(slot)}")
        # ensure required fields
        if not "name" in slot.keys():
            issues.append(f"- no name assigned for slot index {manifest["slots"].index(slot)}")
        if not "mods" in slot.keys():
            issues.append(f"- slot `{slot["name"]}`: enforced mods for this map must be set (`mods` property)")
        if not "map_id" in slot.keys():
            issues.append(f"- slot `{slot["name"]}`: no osu! beatmap was set (`map_id` property)")
        # ensure correct datatype
        if "note" in slot.keys() and not type(slot["note"]) is str:
            issues.append(f"- slot `{slot["name"]}`: `note` property is not a valid note")
        if "force_mod" in slot.keys() and not type(slot["force_mod"]) is bool:
            issues.append(f"- slot `{slot["name"]}`: `force_mod` property is not a valid boolean")
        if "tiebreaker" in slot.keys() and not type(slot["tiebreaker"]) is bool:
            issues.append(f"- slot `{slot["name"]}`: `tiebreaker` property is not a valid boolean")
        if not type(slot["mods"]) is list:
            issues.append(f"- slot `{slot["name"]}`: `mods` property is not a valid list of mods")
        if not type(slot["map_id"]) is int:
            issues.append(f"- slot `{slot["name"]}`: `map_id` is not a valid map ID")
        # ensure beatmap exists
        data = await get_beatmap_data(slot["map_id"])
        if not data:
            issues.append(f"- slot `{slot["name"]}`: specified map ID does NOT exist")
        # ensure no beatmap get reused
        if slot["map_id"] in unique_map_ids.keys():
            issues.append(f"- slot `{slot["name"]}`: specified map ID was used previously in slot `{unique_map_ids[slot["map_id"]]}`")
        else:
            # add to unique map IDs
            unique_map_ids[slot["map_id"]] = slot["name"]
    Logger.info(f"{len(issues)} issue(s) found")
    return issues