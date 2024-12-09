import discord
from discord.ext import commands
from typing import Union, Optional
from io import BytesIO
import logging

logger = logging.getLogger('discord')

def format_pokemon_info(pokemon_data: dict) -> discord.Embed:
    """Formats Pokémon data into a Discord embed message."""
    try:
        name = pokemon_data['name'].title()
        image_url = pokemon_data['sprites']['front_default']
        stats = pokemon_data['stats']
        formatted_stats = format_pokemon_stats(stats)
        embed = discord.Embed(title=name, description=formatted_stats)
        embed.set_thumbnail(url=image_url)
        return embed
    except KeyError as e:
        logger.error(f"Missing key in pokemon data: {e}")
        return discord.Embed(title="Error", description="Could not format Pokémon information.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred while formatting pokemon info: {e}")
        return discord.Embed(title="Error", description="An unexpected error occurred.")


def format_pokemon_stats(stats: list[dict]) -> str:
    """Formats Pokémon stats into a human-readable string."""
    if not stats:
        return "No stats available."
    stat_strings = [f"{stat['stat']['name'].title()}: {stat['base_stat']}" for stat in stats]
    return "\n".join(stat_strings)


def format_error(error: Exception) -> str:
    """Formats an exception into a user-friendly error message."""
    if isinstance(error, requests.exceptions.RequestException):
        return "There was a problem connecting to the Pokémon database. Please try again later."
    elif isinstance(error, KeyError):
        return "Could not find that Pokémon. Please check the spelling."
    elif isinstance(error, discord.errors.HTTPException):
        return "There was a problem sending the message. Please try again later."
    else:
        logger.exception(f"An unexpected error occurred: {error}")
        return "An unexpected error occurred. Please try again later."


async def send_message(ctx: commands.Context, message: Union[str, discord.Embed], image_bytes: Optional[BytesIO] = None) -> None:
    """Sends a message to the Discord channel."""
    try:
        if image_bytes:
            file = discord.File(image_bytes, filename="pokemon.png")
            await ctx.send(embed=message, file=file) if isinstance(message, discord.Embed) else await ctx.send(message, file=file)
        else:
            await ctx.send(embed=message) if isinstance(message, discord.Embed) else await ctx.send(message)
    except discord.errors.HTTPException as e:
        logger.error(f"Error sending message: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred while sending message: {e}")