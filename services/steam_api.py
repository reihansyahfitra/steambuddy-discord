import requests
import json
from config.settings import STEAM_API_KEY, STEAM_STORE_API_URL, STEAM_APP_DETAILS_URL

async def search_steam_games(query):
    """
    Search for games on Steam with the given query.
    Returns the top 5 most popular games matching the query.
    """
    params = {
        "term": query,
        "l": "english",
        "cc": "ID"
    }

    try:
        response = requests.get(STEAM_STORE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Debug: Print the response data
        print(json.dumps(data, indent=4))

        if 'items' in data and len(data['items']) > 0:
            sorted_games = data['items']
            return sorted_games[:5]
        else:
            return []
    except Exception as e:
        print(f"Error searching Steam: {e}")
        return []

async def get_steam_game_details(app_id):
    """
    Fetch detailed information about a specific game by its Steam App ID.
    """
    params = {
        "appids": app_id,
        "cc": "ID",
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
        print(f"Error fetching game details: {e}")
        return None