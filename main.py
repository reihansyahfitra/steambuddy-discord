import os
from services.discord_bot import start_bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    token = os.getenv('TOKEN')
    if not token:
        print("Error: Discord bot token not found. Please add TOKEN to your .env file.")
        exit(1)
    
    print("Starting SteamBuddy Discord bot...")
    start_bot(token)