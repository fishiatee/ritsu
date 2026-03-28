from utils.logger import Logger
from utils.embed import EmbedBuilder
from utils.db import get_linked_user
from match.match import MatchType, Match
from interactions import Extension, SlashContext, slash_command, slash_option, OptionType, SlashCommandChoice, Member, User

class DuelExtension(Extension):
    @slash_command(name="duel",
                   description="Initiate a duel")
    @slash_option(name="discord",
                  description="Who to initiate the duel against",
                  opt_type=OptionType.USER)
    @slash_option(name="pool",
                  description="Pool name or ID",
                  opt_type=OptionType.STRING)
    @slash_option(name="best_of",
                  description="Determines the amount of map that have to be played (default: BO7)",
                  opt_type=OptionType.INTEGER,
                  choices=[
                      SlashCommandChoice(name="BO5 (first to 3)", value=5),
                      SlashCommandChoice(name="BO7 (first to 4)", value=7),
                      SlashCommandChoice(name="BO9 (first to 5)", value=9),
                      SlashCommandChoice(name="BO11 (first to 6)", value=9)])
    async def duel_command(self, ctx: SlashContext, best_of: int, discord: Member | User = None, pool: str = None):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /duel")

        await ctx.defer()

        embed = EmbedBuilder()

        # check if user has linked
        user = await get_linked_user(ctx.author.id)

        if not user:
            embed.set_title("Error")
            embed.add_content("You haven't yet linked your *osu!* profile to your Discord account!\n")
            embed.add_content("**Please do so via the `/link` command before initiating a duel.**")
            await ctx.send(embed=embed.build())
            return
        
        match = Match()
        match.properties.type = MatchType.SOLO
        
        if discord:
            match.properties.type = MatchType.TEAM

            # check if opponent has linked
            opponent = await get_linked_user(discord.id)

            if not opponent:
                embed.set_title("Error")
                embed.add_content("Your opponent doesn't seems to have linked their *osu!* profile to their Discord account yet.\n")
                embed.add_content("**Please tell them to do so via the `/link` command, then try again.**")
                await ctx.send(embed=embed.build())
                return
            
        