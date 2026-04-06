from wrapper.user import search_osu_profiles
from utils import logger
from utils.embed import EmbedBuilder
from database.managers.user import get_linked_user, link_user
from database.manager import DbSession
from interactions import Extension, SlashContext, slash_command, slash_option, OptionType

class DiscordExtension(Extension):
    @slash_command(name="link",
                   description="Link your osu! account")
    @slash_option(name="user_name",
                  description="Your osu! user name",
                  required=True,
                  opt_type=OptionType.STRING)
    async def link_command(self, ctx: SlashContext, user_name: str = None):
        logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /link")

        embed = EmbedBuilder()

        linked_profile = await get_linked_user(ctx.user.id)

        if linked_profile:
            embed.set_title("Error")
            embed.add_content("Your Discord account is already linked to an osu! profile!")
            embed.add_content("Please /unlink it first before linking another one.")
            await ctx.send(embed=embed.build())
            return

        profile = await search_osu_profiles(user_name)

        if not profile:
            embed.set_title("Error")
            embed.add_content("Could not find this username. Please make sure it exists!")
            await ctx.send(embed=embed.build())
            return
        
        logger.verbose(f"(/link) got profile: {profile.username}")
        
        await link_user(ctx.user.id, profile.id)

        embed.set_title("Success!")
        embed.add_content(f"Linked your Discord account to `{profile.username}`!")
        embed.set_thumbnail_image(profile.avatar_url)
        
        await ctx.send(embed=embed.build())

    @slash_command(name="unlink",
                   description="Unlink your osu! account")
    async def unlink_command(self, ctx: SlashContext):
        logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /unlink")

        embed = EmbedBuilder()

        linked_profile = await get_linked_user(ctx.user.id)

        if not linked_profile:
            embed.set_title("Error")
            embed.add_content("You haven't linked any osu! account yet.")
            await ctx.send(embed=embed.build())
            return
        
        db = DbSession()
        await db.remove(linked_profile)
        await db.close()

        embed.set_title("Success!")
        embed.add_content(f"Unlinked your Discord account.")
        
        await ctx.send(embed=embed.build())