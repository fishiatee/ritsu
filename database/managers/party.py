from database.models.party import Party
from database.manager import DbSession
from database.managers.user import get_linked_user
from wrapper.user import get_user_profile

async def create_party(members: list[int] = None, name: str = None) -> Party:
    party = Party()
    party.members = []
    party.leader_id = 0
    if members:
        party.members = members
        party.leader_id = members[0]
    if name:
        party.name = name
    else:
        user = await get_linked_user(party.leader_id)
        profile = await get_user_profile(user.osu_user_id)
        party.name = profile.username
    return await DbSession.add_to_db(party)