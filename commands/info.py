import discord
from discord.ext import commands
import requests
import os
from utils.api_caller import fetch_pokemon_data
from utils.data_formatter import format_pokemon_info
import json

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def info_command(self, ctx, *, pokemon_name: str):
        pokemon_name = pokemon_name.lower()
        try:
            data = await fetch_pokemon_data(pokemon_name)
            if data:
                message = format_pokemon_info(data)
                await ctx.send(message)
            else:
                await ctx.send(f"Could not find Pokémon '{pokemon_name}'. Please check the spelling.")
        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred while fetching data from PokeAPI: {e}")
        except json.JSONDecodeError as e:
            await ctx.send(f"An error occurred while parsing the JSON response: {e}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

async def setup(bot):
    await bot.add_cog(InfoCog(bot))