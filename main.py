import os
from services.discord_bot import start_bot
from dotenv import load_dotenv

# Memuat variabel lingkungan
load_dotenv()

if __name__ == "__main__":
    token = os.getenv('TOKEN')
    if not token:
        print("Error: Token bot Discord tidak ditemukan. Mohon tambahkan TOKEN ke file .env Anda.")
        exit(1)
    
    print("Memulai bot Discord SteamBuddy...")
    start_bot(token)