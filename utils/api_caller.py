import aiohttp
import asyncio
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def fetch_pokemon_data(pokemon_name: str) -> Optional[dict]:
    """Fetches Pokémon data from PokeAPI.

    Args:
        pokemon_name: The name of the Pokémon.

    Returns:
        A dictionary containing the Pokémon's data, or None if an error occurred.
    """
    api_url = f"{os.getenv('POKEAPI_BASE_URL')}pokemon/{pokemon_name}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"PokeAPI request failed with status code: {response.status} for {pokemon_name}")
                    return None
    except aiohttp.ClientError as e:
        logger.error(f"PokeAPI network error: {e} for {pokemon_name}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"PokeAPI JSON decoding error: {e} for {pokemon_name}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching data for {pokemon_name}: {e}")
        return None