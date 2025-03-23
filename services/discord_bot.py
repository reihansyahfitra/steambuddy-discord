import discord
import asyncio
from services.steam_api import search_steam_games
from ui.embeds import format_game_results, create_currency_embed
from utils.user_prefs import set_user_currency, get_user_currency, format_expiry_time, clean_expired_preferences
from config.settings import COMMAND_PREFIX, CURRENCY_PREFIX, SUPPORTED_CURRENCIES

# Menyiapkan intents Discord
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Dipanggil ketika bot siap dan terhubung ke Discord."""
    print(f'Berhasil login sebagai {client.user}')
    print(f'Bot siap menerima perintah {COMMAND_PREFIX}')

    client.loop.create_task(periodic_cleanup())

async def periodic_cleanup():
    """Membersihkan preferensi pengguna yang kedaluwarsa secara berkala."""
    await client.wait_until_ready()
    while not client.is_closed():
        cleaned = clean_expired_preferences()
        if cleaned > 0:
            print(f"Membersihkan {cleaned} preferensi pengguna yang kedaluwarsa")
        await asyncio.sleep(300)  # Berjalan setiap 5 menit

@client.event
async def on_message(message):
    """Menangani pesan masuk dan merespons perintah."""
    # Mengabaikan pesan dari bot sendiri
    if message.author == client.user:
        return

    if message.content.startswith(CURRENCY_PREFIX):
        parts = message.content.split()

        if len(parts) == 1:
            embed = create_currency_embed()
            await message.channel.send(embed=embed)
            return

        if len(parts) > 1:
            currency_code = parts[1].upper()

            if currency_code in SUPPORTED_CURRENCIES:
                set_user_currency(message.author.id, currency_code)
                expiry_time = format_expiry_time(message.author.id)
                currency_name = SUPPORTED_CURRENCIES.get(currency_code, "")
                await message.channel.send(f"✅ Mata uang diubah ke: **{currency_code}** ({currency_name})\nPengaturan akan berlaku hingga **{expiry_time}**")
            else:
                await message.channel.send(
                    f"❌ Kode negara tidak valid. Gunakan `{CURRENCY_PREFIX}` untuk melihat daftar kode negara yang tersedia."
                )
            return

    # Memproses perintah pencarian
    if message.content.startswith(COMMAND_PREFIX):
        # Mengekstrak query dari pesan
        query = message.content[len(COMMAND_PREFIX):].strip()

        if not query:
            await message.channel.send(f"Masukkan nama game yang ingin dicari. Contoh: `{COMMAND_PREFIX} Portal`")
            return

        # Menunjukkan bahwa bot sedang mengetik saat memproses
        async with message.channel.typing():
            # Mendapatkan mata uang pengguna saat ini
            currency_code = get_user_currency(message.author.id)
            currency_name = SUPPORTED_CURRENCIES.get(currency_code, "")
            
            await message.channel.send(f"Mencari: **{query}** (Mata uang: {currency_code} - {currency_name})...")
            
            # Mencari game
            games = await search_steam_games(query, message.author.id)
            
            # Format dan kirim hasil
            embed, view = format_game_results(games, message.author.id)
            
            if games:
                await message.channel.send(embed=embed, view=view)
            else:
                await message.channel.send(embed=embed)

def start_bot(token):
    """Memulai bot Discord dengan token yang diberikan."""
    client.run(token)