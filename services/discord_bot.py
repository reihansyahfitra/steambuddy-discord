import discord
from services.steam_api import search_steam_games
from ui.embeds import format_game_results
from config.settings import COMMAND_PREFIX

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

@client.event
async def on_message(message):
    """Handle incoming messages and respond to commands."""
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Process search command
    if message.content.startswith(COMMAND_PREFIX):
        # Extract query from message
        query = message.content[len(COMMAND_PREFIX):].strip()

        if not query:
            await message.channel.send(f"Please provide a game name to search for. Example: `{COMMAND_PREFIX} Portal`")
            return

        # Indicate that the bot is typing while processing
        async with message.channel.typing():
            await message.channel.send(f"Searching for: **{query}**...")
            
            # Search for games
            games = await search_steam_games(query)
            
            # Format and send results
            embed, view = format_game_results(games)
            
            if games:
                await message.channel.send(embed=embed, view=view)
            else:
                await message.channel.send(embed=embed)

def start_bot(token):
    """Start the Discord bot with the provided token."""
    client.run(token)