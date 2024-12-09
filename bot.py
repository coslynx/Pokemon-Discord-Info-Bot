import discord
from discord.ext import commands
import os
import requests
from PIL import Image
import aiosqlite
import asyncio
import logging

# Configure logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/p!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"commands.{filename[:-3]}")
        except Exception as e:
            logger.exception(f"Failed to load extension {filename}: {e}")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if DISCORD_TOKEN is None:
    logger.critical("DISCORD_TOKEN not found in environment variables!")
    exit(1)

try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
    logger.critical(f"Login failed: {e}")
except discord.errors.HTTPException as e:
    logger.critical(f"HTTP error during connection: {e}")
except Exception as e:
    logger.exception(f"An unexpected error occurred: {e}")