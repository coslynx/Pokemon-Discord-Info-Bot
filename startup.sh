#!/bin/bash

set -euo pipefail

# Check if .env exists
if [ ! -f ".env" ]; then
  echo "Error: .env file not found." >&2
  exit 1
fi

# Source environment variables
source .env

# Activate virtual environment
source .venv/bin/activate

# Log startup
echo "$(date +"%Y-%m-%d %H:%M:%S") Starting Pokémon Generation Bot..." >> bot.log

# Run the bot
python bot.py
EXIT_CODE=$?

# Log errors from bot execution
if [ $EXIT_CODE -ne 0 ]; then
  echo "$(date +"%Y-%m-%d %H:%M:%S") Error: bot.py exited with code $EXIT_CODE." >> bot.log
fi

exit $EXIT_CODE