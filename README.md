<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
Pokémon Generation Bot
</h1>
<h4 align="center">A Discord bot providing Pokémon images and stats.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" alt="Programming Language">
  <img src="https://img.shields.io/badge/Framework-discord.py-red" alt="Discord Bot Library">
  <img src="https://img.shields.io/badge/Database-SQLite-blue" alt="Database">
  <img src="https://img.shields.io/badge/API-PokeAPI-black" alt="External API">
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/Pokemon-Discord-Info-Bot?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/Pokemon-Discord-Info-Bot?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/Pokemon-Discord-Info-Bot?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview
This repository contains the Pokémon Generation Bot, a Discord bot providing users with images and normalized stats (0-31) for all Pokémon across all generations, including shiny variants.  The bot utilizes Python with the `discord.py` library and an SQLite database (optional).  Data is primarily sourced from PokeAPI.

## 📦 Features
|    | Feature                     | Description                                                                                                  |
|----|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| 1  | `/p!info` Command           | Retrieves detailed Pokémon information, including stats and image.                                          |
| 2  | `/p!p` Command              | Displays Pokémon image and normalized stats (0-31). Supports shiny variants using "shiny [Pokémon Name]". |
| 3  | `/p!start` Command          | Provides initial instructions on bot usage.                                                              |
| 4  | Shiny Pokémon Support       | Retrieves and displays both regular and shiny Pokémon variants.                                              |
| 5  | Image Caching               | Caches images locally to reduce API calls and improve performance.                                           |
| 6  | Error Handling              | Includes robust error handling for API failures, invalid input, and missing data.                              |
| 7  | Asynchronous Operations     | Uses asynchronous operations for improved responsiveness and efficiency.                                     |
| 8  | Modular Design              | Follows a modular design with separate files for commands and utility functions.                             |
| 9  | Credit System (Future)      | Foundation laid for a future credit system to enhance user engagement.                                     |
| 10 | Admin Permissions (Future) | Foundation laid for future administrative controls for bot management.                                   |


## 📂 Structure
text
pokemon-generation-bot/
├── bot.py             
├── commands/          
│   ├── info.py        
│   ├── pokemon.py     
│   └── start.py       
├── data/              
│   └── pokemon.db     
├── images/            
├── .env               
├── requirements.txt   
└── tests/
    ├── test_commands.py
    └── test_utils.py



## 💻 Installation
### 🔧 Prerequisites
- Python 3.9+
- `pip`

### 🚀 Setup Instructions
1. Clone the repository:
   bash
   git clone https://github.com/coslynx/Pokemon-Discord-Info-Bot.git
   cd Pokemon-Discord-Info-Bot
   
2. Create a virtual environment (recommended):
   bash
   python3 -m venv .venv
   source .venv/bin/activate
   
3. Install dependencies:
   bash
   pip install -r requirements.txt
   
4. Configure `.env` (replace placeholders with your Discord bot token and PokeAPI base URL):
   
   cp .env.example .env
   


## 🏗️ Usage
1.  Run the bot:
    bash
    python bot.py
    
2.  Invite the bot to your Discord server.
3.  Use the commands: `/p!start`, `/p!p [Pokémon Name]`, `/p!info [Pokémon Name]`

## 🌐 Hosting
Hosting instructions would depend on your chosen platform (e.g., Heroku, AWS, Google Cloud).  A Dockerfile is provided for containerization to facilitate deployment.  Ensure your chosen platform has Python 3.9+, `discord.py` (2.1.0 or later), `requests` (2.31.0 or later), `Pillow` (10.0.0 or later), and `aiosqlite` (0.18.0 or later) installed.  You will also need to set the `DISCORD_TOKEN` and `POKEAPI_BASE_URL` environment variables.

## 📄 License & Attribution

### 📄 License
This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: Pokemon-Discord-Info-Bot

### 📞 Contact
For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
<img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
<img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
<img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
<img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>