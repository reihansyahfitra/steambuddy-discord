import discord
import asyncio
from services.steam_api import search_steam_games
from ui.embeds import format_game_results, create_currency_embed
from utils.user_prefs import set_user_currency, get_user_currency, format_expiry_time, clean_expired_preferences
from config.settings import COMMAND_PREFIX, CURRENCY_PREFIX, SUPPORTED_CURRENCIES

# Set up Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'We have logged in as {client.user}')
    print(f'Bot is ready to receive {COMMAND_PREFIX} commands!')

    client.loop.create_task(periodic_cleanup())

async def periodic_cleanup():
    await client.wait_until_ready()
    while not client.is_closed():
        cleaned = clean_expired_preferences()
        if cleaned > 0:
            print(f"Cleaned up {cleaned} expired user preferences")
        await asyncio.sleep(300)

@client.event
async def on_message(message):
    """Handle incoming messages and respond to commands."""
    # Ignore messages from the bot itself
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
                await message.channel.send(f"Anda telah pindah negara ke: {currency_code}")
            else:
                await message.channel.send(
                    f"❌ NEGARA MANA ITU COK!. Coba pake `{CURRENCY_PREFIX}` buat ngeliat kode-kode nya."
                )

    # Process search command
    if message.content.startswith(COMMAND_PREFIX):
        # Extract query from message
        query = message.content[len(COMMAND_PREFIX):].strip()

        if not query:
            await message.channel.send(f"Tolol. Cara makenya: `{COMMAND_PREFIX} Portal`")
            return

        # Indicate that the bot is typing while processing
        async with message.channel.typing():

            
            await message.channel.send(f"Cooking: **{query}**...")
            
            # Search for games
            games = await search_steam_games(query, message.author.id)
            
            # Format and send results
            embed, view = format_game_results(games, message.author.id)
            
            if games:
                await message.channel.send(embed=embed, view=view)
            else:
                await message.channel.send(embed=embed)

def start_bot(token):
    """Start the Discord bot with the provided token."""
    client.run(token)