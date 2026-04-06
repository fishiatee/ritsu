from utils import logger
from utils.embed import EmbedBuilder
from database.managers.user import get_linked_user
from database.managers.pool import get_pool
from wrapper.user import get_user_profile
from match.match import Match
from main import bot
from interactions import Extension, SlashContext, slash_command, slash_option, OptionType, SlashCommandChoice, Member, User, Button, ButtonStyle

class DuelExtension(Extension):
    @slash_command(name="duel",
                   description="Initiate a duel")
    @slash_option(name="pool_id",
                  description="Pool ID",
                  opt_type=OptionType.STRING,
                  required=True)
    @slash_option(name="opponent",
                  description="Who to initiate the duel against",
                  opt_type=OptionType.USER)
    @slash_option(name="best_of",
                  description="Determines the amount of map that have to be played (default: BO7)",
                  opt_type=OptionType.INTEGER,
                  choices=[
                      SlashCommandChoice(name="BO5 (first to 3)", value=5),
                      SlashCommandChoice(name="BO7 (first to 4)", value=7),
                      SlashCommandChoice(name="BO9 (first to 5)", value=9),
                      SlashCommandChoice(name="BO11 (first to 6)", value=9)])
    async def duel_command(self, ctx: SlashContext, opponent: Member | User = None, pool_id: str = None, best_of: int = 7):
        logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /duel")

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
        
        if opponent:
            # check if opponent has linked
            opponent = await get_linked_user(opponent.id)

            if not opponent:
                embed.set_title("Error")
                embed.add_content("Your opponent doesn't seem to have linked their *osu!* profile to their Discord account yet.\n")
                embed.add_content("**Please tell them to do so via the `/link` command, then try again.**")
                await ctx.send(embed=embed.build())
                return
            
        pool = await get_pool(pool_id)

        if not pool:
            embed.set_title("Error")
            embed.add_content(f"Pool ID `{pool_id}` does not seem to exist.\n")
            embed.add_content("**Please re-check the entered ID, or upload a new pool.**")
            await ctx.send(embed=embed.build())
            return
            
        # TODO: support 2v2/3v3/4v4
        match = await Match.create(pool_id, best_of, ctx.author, opponent)

        embed.set_title("Match Overview")
        
        embed.add_field("Pool", pool.name)
        embed.add_field("Type", match.type)
        embed.add_field("Participant(s)", (await get_user_profile((await get_linked_user(match.teams.party_1.leader_id)).osu_user_id)).username, True)
        if opponent:
            embed.add_field("Opponent(s)", (await get_user_profile((await get_linked_user(match.teams.party_2.leader_id)).osu_user_id)).username, True)
        embed.add_content("Please review the provided information, then click **Ready** to start the match.")

        ready_button = Button(style=ButtonStyle.SECONDARY,
                              label="Ready!")

        message = await ctx.send(embed=embed.build(),
                                 components=[ready_button])
        
        await bot.wait_for_component(messages=message,
                                     components=[ready_button])