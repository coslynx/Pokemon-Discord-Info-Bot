import discord
from discord.ext import commands
import requests
from PIL import Image
from io import BytesIO
from utils.api_caller import fetch_pokemon_data
from utils.image_processor import process_image
from utils.data_formatter import format_pokemon_stats

class PokemonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="p")
    async def pokemon_command(self, ctx, *, pokemon_name: str):
        pokemon_name = pokemon_name.lower()
        try:
            data = await fetch_pokemon_data(pokemon_name)
            if data:
                image_url = data['sprites']['front_default']
                image_bytes = await process_image(image_url)
                formatted_stats = format_pokemon_stats(data['stats'])
                file = discord.File(image_bytes, filename=f"{pokemon_name}.png")
                embed = discord.Embed(title=f"{data['name'].title()} Stats", description=formatted_stats)
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send(f"Pokémon '{pokemon_name}' not found. Please check spelling.")
        except requests.exceptions.RequestException as e:
            await ctx.send(f"Error fetching data: {e}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

async def setup(bot):
    await bot.add_cog(PokemonCommands(bot))