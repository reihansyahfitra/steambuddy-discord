import discord
import requests
from config.settings import STEAMDB_CHARTS_URL, SUPPORTED_CURRENCIES, CURRENCY_SYMBOLS
from utils.helpers import format_price, truncate_text
from utils.user_prefs import get_user_currency

def create_currency_embed():
    """Membuat embed yang menampilkan kode mata uang yang didukung."""
    embed = discord.Embed(
        title="Daftar Kode Mata Uang",
        description="Gunakan `!currency [kode]` untuk mengatur mata uang pilihan Anda",
        color=discord.Color.blue()
    )

    regions = {
        "Amerika": ["US", "AR", "BR", "CA", "CL", "CO", "CR", "MX", "PE", "UY"],
        "Eropa": ["EU", "GB", "NO", "PL", "RU", "TR", "UA"],
        "Asia": ["CN", "HK", "ID", "IN", "JP", "KR", "KZ", "MY", "PH", "SG", "TH", "TW", "VN"],
        "Oseania": ["AU", "NZ"],
        "Timur Tengah & Afrika": ["IL", "QA", "SA", "AE", "ZA"]
    }

    for region, codes in regions.items():
        currencies = []
        for code in codes:
            if code in SUPPORTED_CURRENCIES:
                currencies.append(f"**{code}**: {SUPPORTED_CURRENCIES[code]}")
            
        if currencies:
            embed.add_field(name=region, value="\n".join(currencies), inline=False)

    embed.set_footer(text="Preferensi mata uang Anda akan diingat selama 1 jam")
    return embed

def format_game_results(games, user_id=None):
    """
    Format hasil pencarian ke dalam embed Discord dengan informasi game.
    Mengembalikan embed dan view dengan tombol interaktif.
    """
    from ui.views import GameButtonView  # Import di sini untuk menghindari dependensi sirkular
    
    if not games:
        return discord.Embed(
            title="Game Tidak Ditemukan", 
            description="Tidak ada game yang ditemukan untuk pencarian tersebut",
            color=discord.Color.red()
        ), None

    currency_code = get_user_currency(user_id)
    currency_name = SUPPORTED_CURRENCIES.get(currency_code, "")
    
    embed = discord.Embed(
        title="Top 5 Game",
        description=f"5 game teratas hasil pencarian (Mata Uang: {currency_code} - {currency_name})",
        color=discord.Color.green()
    )

    for i, game in enumerate(games, 1):
        name = game.get('name', 'N/A')
        price = game.get('price', {})

        if price.get('final', 0) == 0:
            price_str = "Gratis"
        else:
            final_price = price.get('final', 0)
            price_str = format_price(final_price, user_id)

            if price.get('discount_percent', 0) > 0:
                original_price = price.get('initial', 0)
                discount = price.get('discount_percent', 0)
                original_price_str = format_price(original_price, user_id)
                price_str = f"~~{original_price_str}~~ {price_str} ({discount}% diskon)"
        
        store_url = f"https://store.steampowered.com/app/{game.get('id', '')}"

        embed.add_field(
            name=f"{i}. {name}",
            value=f"Harga: {price_str}\n[Lihat di Steam]({store_url})",
            inline=False
        )

        if i == 1 and 'tiny_image' in game:
            embed.set_thumbnail(url=game['tiny_image'])
            
    embed.set_footer(text="Klik tombol di bawah untuk informasi detail game")
    
    # Membuat view dengan tombol
    view = GameButtonView(games)
    
    return embed, view

def create_detailed_embed(game_data, basic_game_info, user_id=None):
    """
    Membuat embed detail untuk game dengan format yang kaya dan informatif.
    """
    if not game_data:
        return discord.Embed(
            title="Error",
            description="Gagal mendapatkan detail game",
            color=discord.Color.red()
        )

    currency_code = get_user_currency(user_id)

    # Menentukan warna embed berdasarkan skor metacritic atau menggunakan gradien
    if 'metacritic' in game_data and game_data['metacritic'].get('score'):
        score = game_data['metacritic'].get('score', 0)
        if score >= 80:
            color = discord.Color.from_rgb(66, 200, 66)  # Hijau untuk skor tinggi
        elif score >= 60:
            color = discord.Color.from_rgb(255, 204, 0)  # Kuning/Emas untuk skor menengah
        else:
            color = discord.Color.from_rgb(255, 77, 77)  # Merah untuk skor rendah
    else:
        color = discord.Color.from_rgb(52, 152, 219)  # Biru seperti Steam sebagai default

    # Membuat judul yang stylish dengan emoji
    game_name = basic_game_info.get('name', 'N/A')
    if game_data.get('is_free', False):
        title = f"🎮 {game_name} 🆓"
    else:
        title = f"🎮 {game_name}"

    # Menambahkan deskripsi dari game
    description = game_data.get('short_description', 'Tidak ada deskripsi')
    if description and len(description) > 200:
        description = description[:200] + "..."

    embed = discord.Embed(
        title=title,
        description=f"*{description}*",
        color=color,
        url=f"https://store.steampowered.com/app/{game_data.get('steam_appid', '')}"
    )

    # Gambar header 
    if 'header_image' in game_data:
        embed.set_image(url=game_data['header_image'])

    # Info dasar dengan emoji
    release_date = game_data.get('release_date', {}).get('date', 'Tidak diketahui')
    developer = ", ".join(game_data.get('developers', ['Tidak diketahui']))
    publisher = ", ".join(game_data.get('publishers', ['Tidak diketahui']))
    
    embed.add_field(name="📅 Tanggal Rilis", value=release_date, inline=True)
    embed.add_field(name="💻 Pengembang", value=developer, inline=True)
    embed.add_field(name="🏢 Penerbit", value=publisher, inline=True)

    # Bagian harga dengan format khusus
    price_info = game_data.get('price_overview', {})
    if price_info:
        if price_info.get('final', 0) == 0:
            price_str = "**Gratis**"
        else:
            final_price_cents = price_info.get('final', 0)
            formatted_price = format_price(final_price_cents, user_id)
            price_str = f"**{formatted_price}**"
            
            if price_info.get('discount_percent', 0) > 0:
                initial_price_cents = price_info.get('initial', 0)
                formatted_original = format_price(initial_price_cents, user_id)
                
                discount = price_info.get('discount_percent', 0)
                price_str = f"~~{formatted_original}~~ **{formatted_price}** 🔥 **{discount}% DISKON!**"
    else:
        symbol = CURRENCY_SYMBOLS.get(currency_code, "$")
        price_str = f"*Harga tidak tersedia*"
    
    embed.add_field(name="💰 Harga", value=price_str, inline=True)

    # Skor Metacritic dengan format warna
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
            metacritic_value = "*Tidak ada skor*"
            
        embed.add_field(name="📊 Skor Metacritic", value=metacritic_value, inline=True)
    else:
        embed.add_field(name="📊 Skor Metacritic", value="*Tidak ada skor*", inline=True)
    
    # Jumlah pemain
    app_id = game_data.get('steam_appid', '')
    steamdb_url = f"{STEAMDB_CHARTS_URL}{app_id}/charts/"
    embed.add_field(
        name="👥 Statistik Pemain", 
        value=f"[**Lihat Grafik Jumlah Pemain**]({steamdb_url})", 
        inline=True
    )

    # Kategori dengan format khusus
    categories = [cat.get('description', '') for cat in game_data.get('categories', [])[:6]]
    if categories:
        cat_str = " • ".join([f"**{cat}**" for cat in categories])
        embed.add_field(name="🏷️ Kategori", value=cat_str, inline=False)

    # Genre dengan indikator emoji
    genres = [genre.get('description', '') for genre in game_data.get('genres', [])]
    if genres:
        genre_str = " • ".join([f"**{genre}**" for genre in genres])
        embed.add_field(name="🎯 Genre", value=genre_str, inline=False)
    
    # Persyaratan sistem (disingkat)
    if 'pc_requirements' in game_data and 'minimum' in game_data['pc_requirements']:
        min_req = game_data['pc_requirements']['minimum']
        # Menghilangkan tag HTML untuk tampilan yang lebih bersih
        min_req = min_req.replace('<br>', '\n').replace('<strong>', '**').replace('</strong>', '**')
        min_req = min_req[:250] + "..." if len(min_req) > 250 else min_req
        embed.add_field(name="💻 Spesifikasi Minimum", value=f"[Lihat Persyaratan Lengkap](https://store.steampowered.com/app/{app_id})", inline=False)
    
    # Tag jika tersedia
    if 'tags' in game_data and len(game_data['tags']) > 0:
        tags = [tag[:12] for tag in game_data['tags'][:8]]
        tag_str = ", ".join([f"`{tag}`" for tag in tags])
        embed.add_field(name="🔖 Tag Populer", value=tag_str, inline=False)
    
    # Bagian tautan
    links_value = f"[Halaman Steam](https://store.steampowered.com/app/{app_id}) • [SteamDB](https://steamdb.info/app/{app_id}) • [PCGamingWiki](https://www.pcgamingwiki.com/api/appid.php?appid={app_id})"
    embed.add_field(name="🔗 Tautan", value=links_value, inline=False)

    # Footer dengan ID app dan Steam
    embed.set_footer(text=f"Steam AppID: {app_id} | Diberdayakan oleh Steam")
    
    return embed