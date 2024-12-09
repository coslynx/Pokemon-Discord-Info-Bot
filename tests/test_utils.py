import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from utils.api_caller import fetch_pokemon_data
from utils.image_processor import process_image
from utils.message_handler import format_pokemon_info, format_pokemon_stats, format_error, send_message
from utils.data_formatter import format_pokemon_stats as df_format_pokemon_stats
from PIL import Image
import io
import aiohttp
import requests
import discord

@pytest.mark.asyncio
async def test_fetch_pokemon_data_success():
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {'name': 'Pikachu', 'stats': [{'base_stat': 60}]}
    mock_session.get.return_value = mock_response

    with patch('utils.api_caller.aiohttp.ClientSession', return_value=mock_session):
        data = await fetch_pokemon_data('pikachu')
        assert data['name'] == 'Pikachu'
        assert data['stats'][0]['base_stat'] == 60
        mock_session.get.assert_called_once_with('https://pokeapi.co/api/v2/pokemon/pikachu')

@pytest.mark.asyncio
async def test_fetch_pokemon_data_failure():
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_session.get.return_value = mock_response
    with patch('utils.api_caller.aiohttp.ClientSession', return_value=mock_session):
        data = await fetch_pokemon_data('invalid-pokemon')
        assert data is None

@pytest.mark.asyncio
async def test_fetch_pokemon_data_client_error():
    mock_session = AsyncMock()
    mock_session.get.side_effect = aiohttp.ClientError()
    with patch('utils.api_caller.aiohttp.ClientSession', return_value=mock_session):
        data = await fetch_pokemon_data('pikachu')
        assert data is None

@pytest.mark.asyncio
async def test_fetch_pokemon_data_json_error():
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.side_effect = json.JSONDecodeError('error','doc',1)
    mock_session.get.return_value = mock_response
    with patch('utils.api_caller.aiohttp.ClientSession', return_value=mock_session):
        data = await fetch_pokemon_data('pikachu')
        assert data is None


@patch('utils.image_processor.requests.get')
def test_process_image_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'image data'
    image_bytes = process_image('test_url')
    assert image_bytes is not None

@patch('utils.image_processor.requests.get')
def test_process_image_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException('Network error')
    image_bytes = process_image('test_url')
    assert image_bytes is None

@patch('utils.image_processor.requests.get')
def test_process_image_ioerror(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'corrupted data'
    image_bytes = process_image('test_url')
    assert image_bytes is None

def test_format_pokemon_info_success():
    data = {'name': 'Pikachu', 'sprites': {'front_default': 'url'}, 'stats': [{'stat': {'name': 'hp'}, 'base_stat': 100}]}
    embed = format_pokemon_info(data)
    assert isinstance(embed, discord.Embed)
    assert embed.title == 'Pikachu'

def test_format_pokemon_info_failure():
    data = {'name': 'Pikachu'}
    embed = format_pokemon_info(data)
    assert isinstance(embed, discord.Embed)
    assert embed.title == "Error"

def test_format_pokemon_stats_success():
    stats = [{'stat': {'name': 'hp'}, 'base_stat': 100}, {'stat': {'name': 'attack'}, 'base_stat': 80}]
    formatted_stats = format_pokemon_stats(stats)
    assert "HP: 100\nAttack: 80" in formatted_stats

def test_format_pokemon_stats_empty():
    formatted_stats = format_pokemon_stats([])
    assert formatted_stats == "No stats available."

def test_format_pokemon_stats_invalid():
    stats = "invalid"
    formatted_stats = df_format_pokemon_stats(stats)
    assert formatted_stats == "No stats available."

def test_format_error_request_exception():
    error = requests.exceptions.RequestException("Network error")
    message = format_error(error)
    assert message == "There was a problem connecting to the Pokémon database. Please try again later."

def test_format_error_key_error():
    error = KeyError("Missing key")
    message = format_error(error)
    assert message == "Could not find that Pokémon. Please check the spelling."

def test_format_error_http_exception():
    error = discord.errors.HTTPException("HTTP error")
    message = format_error(error)
    assert message == "There was a problem sending the message. Please try again later."

def test_format_error_other_exception():
    error = Exception("Other error")
    message = format_error(error)
    assert "An unexpected error occurred" in message

@pytest.mark.asyncio
async def test_send_message_success(mocker):
    ctx = AsyncMock()
    await send_message(ctx, "Test message")
    ctx.send.assert_called_once_with("Test message")

@pytest.mark.asyncio
async def test_send_message_embed(mocker):
    ctx = AsyncMock()
    embed = discord.Embed(title="Test Embed")
    await send_message(ctx, embed)
    ctx.send.assert_called_once_with(embed=embed)

@pytest.mark.asyncio
async def test_send_message_image(mocker):
    ctx = AsyncMock()
    image_bytes = io.BytesIO(b'image data')
    await send_message(ctx, "Test message", image_bytes)
    ctx.send.assert_called_once()

@pytest.mark.asyncio
async def test_send_message_http_exception(mocker):
    ctx = AsyncMock()
    ctx.send.side_effect = discord.errors.HTTPException("HTTP error")
    await send_message(ctx, "Test message")
    ctx.send.assert_called_once()