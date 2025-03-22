import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Steam API settings
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
STEAM_STORE_API_URL = "https://store.steampowered.com/api/storesearch/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails/"
STEAMDB_CHARTS_URL = "https://steamdb.info/app/"

# Discord bot settings
COMMAND_PREFIX = "!search"
BOT_TIMEOUT = 120  # Timeout for interactive components in seconds