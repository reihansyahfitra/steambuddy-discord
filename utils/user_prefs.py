import time
from datetime import datetime
from config.settings import DEFAULT_CURRENCY, USER_CURRENCY_TIMEOUT

user_preferences = {}

def get_user_currency(user_id):
    if user_id in user_preferences:
        timestamp = user_preferences[user_id]['timestamp']
        current_time = time.time()

        if current_time - timestamp < USER_CURRENCY_TIMEOUT:
            return user_preferences[user_id]['currency']
        else:
            del user_preferences[user_id]
    return DEFAULT_CURRENCY

def set_user_currency(user_id, currency):
    user_preferences[user_id] = {
        'currency': currency.upper(),
        'timestamp': time.time()
    }
    return user_preferences[user_id]['currency']

def format_expiry_time(user_id):
    if user_id not in user_preferences:
        return None
    
    timestamp = user_preferences[user_id]['timestamp']
    expiry_time = timestamp + USER_CURRENCY_TIMEOUT
    expiry_datetime = datetime.fromtimestamp(expiry_time)

    return expiry_datetime.strftime("%H:%M:%S")

def clean_expired_preferences():
    current_time = time.time()
    expired_users = []

    for user_id, prefs in user_preferences.items():
        if current_time - prefs['timestamp'] >= USER_CURRENCY_TIMEOUT:
            expired_users.append(user_id)
        
    for user_id in expired_users:
        del user_preferences[user_id]

    return len(expired_users)