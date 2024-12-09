import discord
from typing import List, Dict, Union
import logging

logger = logging.getLogger(__name__)

def format_pokemon_info(pokemon_data: Dict[str, Union[str, List, Dict]]) -> discord.Embed:
    """Formats Pokémon data into a Discord embed message.

    Args:
        pokemon_data: A dictionary containing Pokémon data.

    Returns:
        A discord.Embed object containing the formatted Pokémon information, 
        or an error embed if data is missing or invalid.
    """
    try:
        name = pokemon_data['name'].title()
        image_url = pokemon_data['sprites']['front_default']
        stats = pokemon_data['stats']
        formatted_stats = format_pokemon_stats(stats)
        embed = discord.Embed(title=name, description=formatted_stats)
        embed.set_thumbnail(url=image_url)
        return embed
    except KeyError as e:
        logger.error(f"Missing key in pokemon data: {e}, data: {pokemon_data}")
        return discord.Embed(title="Error", description="Could not format Pokémon information. Missing key.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred while formatting pokemon info: {e}")
        return discord.Embed(title="Error", description="An unexpected error occurred.")


def format_pokemon_stats(stats: List[Dict[str, Union[str, int]]]) -> str:
    """Formats Pokémon stats into a human-readable string.

    Args:
        stats: A list of dictionaries, where each dictionary represents a stat.

    Returns:
        A formatted string representing the Pokémon's stats, or "No stats available." if the input is invalid.
    """
    if not stats or not isinstance(stats, list):
        return "No stats available."
    stat_strings = [f"{stat['stat']['name'].title()}: {stat['base_stat']}" for stat in stats if isinstance(stat, dict) and 'stat' in stat and 'base_stat' in stat]
    return "\n".join(stat_strings)