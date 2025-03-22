import discord
from discord.ui import View, Button
from services.steam_api import get_steam_game_details
from ui.embeds import create_detailed_embed
from utils.helpers import truncate_text

class GameButtonView(View):
    """
    Creates interactive buttons for each game in search results.
    Each button shows detailed information about its game when clicked.
    """
    def __init__(self, games):
        super().__init__(timeout=120)  # Buttons expire after 2 minutes
        
        # Add a button for each game
        for i, game in enumerate(games, 1):
            game_name = truncate_text(game.get('name', 'Game'), max_length=70, add_ellipsis=True)
            button = Button(
                label=f"Info: {game_name}",
                style=discord.ButtonStyle.primary,
                custom_id=f"game_info_{game.get('id', '')}"
            )
            button.callback = self.create_button_callback(game)
            self.add_item(button)
    
    def create_button_callback(self, game):
        """Creates a callback function for each button."""
        async def button_callback(interaction):
            # Let the user know we're processing
            await interaction.response.defer(ephemeral=True)
            
            # Get game ID
            game_id = game.get('id', '')
            if not game_id:
                await interaction.followup.send("Error: Could not find game ID", ephemeral=True)
                return
            
            # Fetch detailed game info
            game_details = await get_steam_game_details(game_id)
            
            # Create and send detailed embed
            embed = create_detailed_embed(game_details, game)
            await interaction.followup.send(embed=embed, ephemeral=False)
        
        return button_callback