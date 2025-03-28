import requests
import json
from config.settings import STEAM_API_KEY, STEAM_STORE_API_URL, STEAM_APP_DETAILS_URL
from utils.user_prefs import get_user_currency

async def search_steam_games(query, user_id=None):
    """
    Mencari game di Steam dengan query yang diberikan.
    Mengembalikan 5 game paling populer yang cocok dengan query.
    """
    # Dapatkan mata uang pilihan pengguna
    currency_code = get_user_currency(user_id) if user_id else "ID"
    
    params = {
        "term": query,
        "l": "english",
        "cc": currency_code
    }

    try:
        response = requests.get(STEAM_STORE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            sorted_games = data['items']
            return sorted_games[:5]
        else:
            return []
    except Exception as e:
        print(f"Error mencari game di Steam: {e}")
        return []

async def get_steam_game_details(app_id, user_id=None):
    """
    Mengambil informasi detail tentang game tertentu berdasarkan ID App Steam.
    """
    # Dapatkan mata uang pilihan pengguna
    currency_code = get_user_currency(user_id) if user_id else "ID"
    
    params = {
        "appids": app_id,
        "cc": currency_code,
        "l": "english"
    }

    try:
        response = requests.get(STEAM_APP_DETAILS_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if str(app_id) in data and data[str(app_id)].get('success', False):
            return data[str(app_id)]['data']
        else:
            return None
    except Exception as e:
        print(f"Error mengambil detail game: {e}")
        return None