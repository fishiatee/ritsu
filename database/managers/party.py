from database.models.party import Party
from database.manager import DbSession
from utils.misc import gen_hex_str

async def create_party(members: list[int], name: str = None) -> Party:
    session = DbSession()
    party = Party()
    if name:
        party.name = name
    else:
        party.name = f"RITSU_AUTO-PARTY_{gen_hex_str(10)}"
    party.members = members
    party.leader_id = members[0]
    await session.add_or_update(party)
    await session.close()
    return party