import discord
import requests
from config.settings import STEAMDB_CHARTS_URL, SUPPORTED_CURRENCIES, CURRENCY_SYMBOLS
from utils.helpers import format_price, truncate_text
from utils.user_prefs import get_user_currency

def create_currency_embed():
    embed = discord.Embed(
        title="Kode negara yang ada",
        description="Gunakan `!currency [kode]` untuk mengatur mata uangmu",
        color=discord.Color.blue()
    )

    regions = {
        "Americas": ["US", "AR", "BR", "CA", "CL", "CO", "CR", "MX", "PE", "UY"],
        "Europe": ["EU", "GB", "NO", "PL", "RU", "TR", "UA"],
        "Asia": ["CN", "HK", "ID", "IN", "JP", "KR", "KZ", "MY", "PH", "SG", "TH", "TW", "VN"],
        "Oceania": ["AU", "NZ"],
        "Middle East & Africa": ["IL", "QA", "SA", "AE", "ZA"]
    }

    for region, codes in regions.items():
        currencies = []
        for code in codes:
            if code in SUPPORTED_CURRENCIES:
                currencies.append(f"{code}: {SUPPORTED_CURRENCIES[code]}")
            
        if currencies:
            embed.add_field(name=region, value="\n".join(currencies), inline=False)

    return embed

def format_game_results(games, user_id=None):
    """
    Format search results into a Discord embed with game information.
    Returns both the embed and a view with interactive buttons.
    """
    from ui.views import GameButtonView  # Import here to avoid circular dependency
    
    if not games:
        return discord.Embed(
            title="Ngawur", 
            description="Gaada game yang ketemu",
            color=discord.Color.red()
        ), None

    currency_code = get_user_currency(user_id)
    currency_name = SUPPORTED_CURRENCIES.get(currency_code, "")
    
    embed = discord.Embed(
        title="Top 5 Game",
        description=f"5 game paling gacor di Steam (Negara: {currency_name})",
        color=discord.Color.green()
    )

    for i, game in enumerate(games, 1):
        name = game.get('name', 'N/A')
        price = game.get('price', {})

        if price.get('final', 0) == 0:
            price_str = "GRATIS COY!"
        else:
            final_price = price.get('final', 0)
            price_str = format_price(final_price, user_id)

            if price.get('discount_percent', 0) > 0:
                original_price = price.get('initial', 0)
                discount = price.get('discount_percent', 0)
                original_price_str = format_price(original_price, user_id)
                price_str = f"~~{original_price_str}~~ {price_str} ({discount}% off)"
        
        store_url = f"https://store.steampowered.com/app/{game.get('id', '')}"

        embed.add_field(
            name=f"{i}. {name}",
            value=f"Harga: {price_str}\n[Gas ke Steam]({store_url})",
            inline=False
        )

        if i == 1 and 'tiny_image' in game:
            embed.set_thumbnail(url=game['tiny_image'])
            
    embed.set_footer(text="Tekan tombol di bawah jika Anda gay")
    
    # Create view with buttons
    view = GameButtonView(games)
    
    return embed, view

def create_detailed_embed(game_data, basic_game_info, user_id=None):
    """
    Create a detailed embed for a single game with rich formatting and information.
    """
    if not game_data:
        return discord.Embed(
            title="LAH!",
            description="Game yang dicari gaada",
            color=discord.Color.red()
        )

    currency_code = get_user_currency(user_id)

    # Determine embed color based on metacritic score or use a gradient
    if 'metacritic' in game_data and game_data['metacritic'].get('score'):
        score = game_data['metacritic'].get('score', 0)
        if score >= 80:
            color = discord.Color.from_rgb(66, 200, 66)  # Green for high scores
        elif score >= 60:
            color = discord.Color.from_rgb(255, 204, 0)  # Yellow/Gold for medium scores
        else:
            color = discord.Color.from_rgb(255, 77, 77)  # Red for low scores
    else:
        color = discord.Color.from_rgb(52, 152, 219)  # Steam-like blue as default

    # Create stylish title with emojis
    game_name = basic_game_info.get('name', 'N/A')
    if game_data.get('is_free', False):
        title = f"🎮 {game_name} 🆓"
    else:
        title = f"🎮 {game_name}"

    embed = discord.Embed(
        title=title,
        description="*lu gay*",
        color=color,
        url=f"https://store.steampowered.com/app/{game_data.get('steam_appid', '')}"
    )

    # Header image with backdrop effect (using thumbnail + image)
    if 'header_image' in game_data:
        embed.set_image(url=game_data['header_image'])

    # Basic info with emojis
    release_date = game_data.get('release_date', {}).get('date', 'Unknown')
    developer = ", ".join(game_data.get('developers', ['Unknown']))
    publisher = ", ".join(game_data.get('publishers', ['Unknown']))
    
    embed.add_field(name="📅 Kapan dimasak", value=release_date, inline=True)
    embed.add_field(name="💻 Pemasak", value=developer, inline=True)
    embed.add_field(name="🏢 Penyaji", value=publisher, inline=True)

    # Price section with special formatting
    price_info = game_data.get('price_overview', {})
    if price_info:
        if price_info.get('final', 0) == 0:
            price_str = "**GRATIS COY!**"
        else:
            final_price_cents = price_info.get('final', 0)
            formatted_price = format_price(final_price_cents, user_id)
            price_str = f"**{formatted_price}**"
            
            if price_info.get('discount_percent', 0) > 0:
                initial_price_cents = price_info.get('initial', 0)
                formatted_original = format_price(initial_price_cents, user_id)
                
                discount = price_info.get('discount_percent', 0)
                price_str = f"~~{formatted_original}~~ **{formatted_price}** 🔥 **{discount}% OFF!**"
    else:
        symbol = CURRENCY_SYMBOLS.get(currency_code, "$")
        price_str = f"{symbol} 💀"
    
    embed.add_field(name="💰 Harga", value=price_str, inline=True)

    # Metacritic score with color formatting
    if 'metacritic' in game_data:
        score = game_data['metacritic'].get('score', 'N/A')
        url = game_data['metacritic'].get('url', '')
        
        if score != 'N/A':
            if int(score) >= 80:
                metacritic_value = f"[**{score}/100** 🌟]({url})"
            elif int(score) >= 60:
                metacritic_value = f"[**{score}/100** ⭐]({url})"
            else:
                metacritic_value = f"[**{score}/100** ☆]({url})"
        else:
            metacritic_value = "*0/0*"
            
        embed.add_field(name="📊 Nilai", value=metacritic_value, inline=True)
    else:
        embed.add_field(name="📊 Nilai", value="*0/0*", inline=True)
    
    # Player counts if available
    app_id = game_data.get('steam_appid', '')
    steamdb_url = f"{STEAMDB_CHARTS_URL}{app_id}/charts/"
    embed.add_field(
        name="👥 Pemain", 
        value=f"[**Klik disini untuk melihat chart**]({steamdb_url})", 
        inline=True
    )

    # Categories with special formatting
    categories = [cat.get('description', '') for cat in game_data.get('categories', [])[:6]]
    if categories:
        cat_str = " • ".join([f"**{cat}**" for cat in categories])
        embed.add_field(name="🏷️ Kategori", value=cat_str, inline=False)

    # Genres with emoji indicators
    genres = [genre.get('description', '') for genre in game_data.get('genres', [])]
    if genres:
        genre_str = " • ".join([f"**{genre}**" for genre in genres])
        embed.add_field(name="🎯 Genre", value=genre_str, inline=False)
    
    # System requirements (shortened)
    if 'pc_requirements' in game_data and 'minimum' in game_data['pc_requirements']:
        min_req = game_data['pc_requirements']['minimum']
        # Strip HTML tags for cleaner display
        min_req = min_req.replace('<br>', '\n').replace('<strong>', '**').replace('</strong>', '**')
        min_req = min_req[:250] + "..." if len(min_req) > 250 else min_req
        embed.add_field(name="💻 PC kentang renungin aja", value=f"[Lihat disini untuk meratapi betapa kentangnya PC mu](https://store.steampowered.com/app/{app_id})", inline=False)
    
    # Tags if available
    if 'tags' in game_data and len(game_data['tags']) > 0:
        tags = [tag[:12] for tag in game_data['tags'][:8]]
        tag_str = ", ".join([f"`{tag}`" for tag in tags])
        embed.add_field(name="🔖 Popular Tags", value=tag_str, inline=False)
    
    # Links section
    links_value = f"[GAS BELI](https://store.steampowered.com/app/{app_id}) • [SteamDB](https://steamdb.info/app/{app_id}) • [PCGamingWiki](https://www.pcgamingwiki.com/api/appid.php?appid={app_id})"
    embed.add_field(name="🔗 Ling", value=links_value, inline=False)

    # Footer with app ID and Steam logo mention
    embed.set_footer(text=f"Steam AppID: {app_id} | Powered by Steam")
    
    return embed