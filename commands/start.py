import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')

class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start")
    async def start_command(self, ctx):
        help_message = """
        Welcome to the Pokémon Generation Bot!

        Use these commands to get Pokémon information:
        `/p!p [Pokémon Name]` - Shows the Pokémon image and stats.  For shiny Pokémon, use `/p!p shiny [Pokémon Name]`
        `/p!info [Pokémon Name]` - Shows detailed Pokémon information.

        Have fun!
        """
        await ctx.send(help_message)
        logger.info(f"/p!start command used by {ctx.author} in {ctx.channel}")

async def setup(bot):
    await bot.add_cog(StartCog(bot))