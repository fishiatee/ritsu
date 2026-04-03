import yaml
from utils import logger
from utils.embed import EmbedBuilder
from utils.db import get_pool_by_id, get_slot_by_id
from pool.validator import validate_pool
from pool.manager import build_pool
from pool.utils import calculate_avg_sr, calculate_sr
from wrapper.beatmap import get_beatmap_data
from interactions import Extension, SlashContext, slash_command, slash_option, OptionType, Attachment
from httpx import AsyncClient
from yaml.parser import ParserError

class PoolExtension(Extension):
    @slash_command(name="upload-pool",
                   description="Upload a pool for use in duels")
    @slash_option(name="manifest",
                  description="Pool .yml/.yaml file",
                  required=True,
                  opt_type=OptionType.ATTACHMENT)
    async def upload_pool_command(self, ctx: SlashContext, manifest: Attachment):
        logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /upload-pool")

        await ctx.defer()

        embed = EmbedBuilder()

        async with AsyncClient() as client:
            yml = await client.get(manifest.url)

        try:
            pool_data = yaml.safe_load(yml.content)
        except ParserError:
            embed.set_title("Error")
            embed.add_content("**The manifest file you've attached seems to be malformed.**\n")
            embed.add_content("Please make sure your pool manifest is correctly written. Using a YAML validator may help with fixing it.")
            await ctx.send(embed=embed.build())
            return
        
        logger.verbose(f"(/upload-pool) manifest content: {pool_data}")
        
        validation_results = await validate_pool(pool_data)

        if len(validation_results) > 0:
            embed.set_title("Error")
            embed.add_content("One or more issues were detected in the uploaded pool manifest file. Please correct them first, then try uploading the file again.\n")
            embed.add_content("**Detected issues:**")
            for issue in validation_results:
                embed.add_content(issue)
            await ctx.send(embed=embed.build())
            return

        # build pool object & add to db
        id = await build_pool(pool_data, ctx.user.id)
        pool = await get_pool_by_id(id)

        # calculate average pool sr
        avg_sr = await calculate_avg_sr(pool.slots.values())
        
        # embed
        embed.set_header("Added new pool to Ritsu!")
        embed.set_footer(f"Pool ID: {pool.pool_id}")
        embed.set_title(pool.name)
        embed.add_content("**Description**")
        embed.add_content(pool.description)
        embed.add_content("")       # new line
        embed.add_content(f"**Slots** (average SR: **{round(avg_sr, 2)}**★)")
        for name, id in pool.slots.items():
            slot = await get_slot_by_id(id)
            data = await get_beatmap_data(slot.map_id)
            sr = await calculate_sr(slot)
            embed.add_content(f"- `{name}` {data.beatmapset.artist} - {data.beatmapset.title} ({data.version}) [**{round(sr, 2)}**★]")
        
        # send
        await ctx.send(embed=embed.build())