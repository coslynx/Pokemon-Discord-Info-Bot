import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from discord.ext import commands
from commands.info import InfoCog
from commands.pokemon import PokemonCommands
from commands.start import StartCog
from utils.api_caller import fetch_pokemon_data
from utils.image_processor import process_image
from utils.data_formatter import format_pokemon_info, format_pokemon_stats
import requests
import discord


@pytest.mark.asyncio
async def test_info_command_valid_pokemon(mocker):
    mock_fetch_pokemon_data = mocker.patch('utils.api_caller.fetch_pokemon_data', return_value={'name': 'Pikachu', 'sprites': {'front_default': 'url'}, 'stats': [{'stat': {'name': 'hp'}, 'base_stat': 100}]})
    mock_format_pokemon_info = mocker.patch('utils.data_formatter.format_pokemon_info', return_value=discord.Embed(title='Pikachu', description='hp: 100'))
    bot = commands.Bot(command_prefix="/p!")
    info_cog = InfoCog(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await info_cog.info_command(ctx, pokemon_name="Pikachu")
    mock_fetch_pokemon_data.assert_called_once_with("pikachu")
    mock_format_pokemon_info.assert_called_once()
    ctx.send.assert_called_once()


@pytest.mark.asyncio
async def test_info_command_invalid_pokemon(mocker):
    mocker.patch('utils.api_caller.fetch_pokemon_data', return_value=None)
    bot = commands.Bot(command_prefix="/p!")
    info_cog = InfoCog(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await info_cog.info_command(ctx, pokemon_name="NonExistentPokemon")
    ctx.send.assert_called_once_with("Could not find Pokémon 'nonexistentpokemon'. Please check the spelling.")


@pytest.mark.asyncio
async def test_info_command_api_error(mocker):
    mocker.patch('utils.api_caller.fetch_pokemon_data', side_effect=requests.exceptions.RequestException("API Error"))
    bot = commands.Bot(command_prefix="/p!")
    info_cog = InfoCog(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await info_cog.info_command(ctx, pokemon_name="Pikachu")
    ctx.send.assert_called_once_with("An error occurred while fetching data from PokeAPI: API Error")



@pytest.mark.asyncio
async def test_pokemon_command_valid_pokemon(mocker):
    mock_fetch_pokemon_data = mocker.patch('utils.api_caller.fetch_pokemon_data', return_value={'name': 'Pikachu', 'sprites': {'front_default': 'url'}, 'stats': [{'stat': {'name': 'hp'}, 'base_stat': 100}]})
    mock_process_image = mocker.patch('utils.image_processor.process_image', return_value=io.BytesIO(b'image_data'))
    mock_format_pokemon_stats = mocker.patch('utils.data_formatter.format_pokemon_stats', return_value='hp: 100')
    bot = commands.Bot(command_prefix="/p!")
    pokemon_cog = PokemonCommands(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await pokemon_cog.pokemon_command(ctx, pokemon_name="Pikachu")
    mock_fetch_pokemon_data.assert_called_once_with("pikachu")
    mock_process_image.assert_called_once()
    mock_format_pokemon_stats.assert_called_once()
    ctx.send.assert_called_once()


@pytest.mark.asyncio
async def test_pokemon_command_invalid_pokemon(mocker):
    mocker.patch('utils.api_caller.fetch_pokemon_data', return_value=None)
    bot = commands.Bot(command_prefix="/p!")
    pokemon_cog = PokemonCommands(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await pokemon_cog.pokemon_command(ctx, pokemon_name="NonExistentPokemon")
    ctx.send.assert_called_once_with("Pokémon 'nonexistentpokemon' not found. Please check spelling.")


@pytest.mark.asyncio
async def test_pokemon_command_api_error(mocker):
    mocker.patch('utils.api_caller.fetch_pokemon_data', side_effect=requests.exceptions.RequestException("API Error"))
    bot = commands.Bot(command_prefix="/p!")
    pokemon_cog = PokemonCommands(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await pokemon_cog.pokemon_command(ctx, pokemon_name="Pikachu")
    ctx.send.assert_called_once_with("Error fetching data: API Error")


@pytest.mark.asyncio
async def test_pokemon_command_image_error(mocker):
    mocker.patch('utils.api_caller.fetch_pokemon_data', return_value={'name': 'Pikachu', 'sprites': {'front_default': 'url'}, 'stats': [{'stat': {'name': 'hp'}, 'base_stat': 100}]})
    mocker.patch('utils.image_processor.process_image', return_value=None)
    bot = commands.Bot(command_prefix="/p!")
    pokemon_cog = PokemonCommands(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await pokemon_cog.pokemon_command(ctx, pokemon_name="Pikachu")
    ctx.send.assert_called_once() #Should send an error message - needs improvement in actual function



@pytest.mark.asyncio
async def test_start_command(mocker):
    bot = commands.Bot(command_prefix="/p!")
    start_cog = StartCog(bot)
    ctx = mocker.AsyncMock(spec=commands.Context)
    await start_cog.start_command(ctx)
    ctx.send.assert_called_once()

import io