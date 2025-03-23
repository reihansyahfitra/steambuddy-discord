# SteamBuddy Discord Bot

SteamBuddy is a Discord bot that helps you easily gets Steam games details.

## Features (for now)

- **Game Search**: Find some games.
- **Game Details**: Get detailed information about a specific game.

## Installation

To install and run the SteamBuddy Discord bot, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/reihansyahfitra/steambuddy-discord.git
   ```
2. Navigate to the project directory
   ```
   cd steambuddy-discord
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a .env file and add your Discord bot token and Steam API key:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   STEAM_API_KEY=your_steam_api_key
   ```
5. Run the bot:
   ```
   python bot.py
   ```
## Usage

Once the bot is running, you can use the following commands in your Discord server:
- ```!search <game_name>```: Find top 5 games from given parameters and provide the details on the game you clicked.
- ```!currency```: Display the list of country code.
- ```!currency <country_code>```: Change the regional price and the currency symbol on the game prices.
