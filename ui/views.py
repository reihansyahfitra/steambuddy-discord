import discord
from discord.ui import View, Button
from services.steam_api import get_steam_game_details
from ui.embeds import create_detailed_embed
from utils.helpers import truncate_text

class GameButtonView(View):
    """
    Membuat tombol interaktif untuk setiap game dalam hasil pencarian.
    Setiap tombol menampilkan informasi detail tentang game saat diklik.
    """
    def __init__(self, games):
        super().__init__(timeout=120)  # Tombol kedaluwarsa setelah 2 menit
        
        # Menambahkan tombol untuk setiap game
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
        """Membuat fungsi callback untuk setiap tombol."""
        async def button_callback(interaction):
            # Memberi tahu pengguna bahwa kita sedang memproses
            await interaction.response.defer(ephemeral=True)
            
            # Mendapatkan ID game
            game_id = game.get('id', '')
            if not game_id:
                await interaction.followup.send("Error: ID game tidak ditemukan", ephemeral=True)
                return

            user_id = interaction.user.id
            
            # Mengambil informasi detail game
            game_details = await get_steam_game_details(game_id, user_id)
            
            # Membuat dan mengirim embed detail
            embed = create_detailed_embed(game_details, game, user_id)
            await interaction.followup.send(embed=embed, ephemeral=False)
        
        return button_callback