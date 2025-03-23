import time
from datetime import datetime
from config.settings import DEFAULT_CURRENCY, USER_CURRENCY_TIMEOUT

# Kamus untuk menyimpan preferensi mata uang pengguna
# Format: {user_id: {"currency": "US", "timestamp": 1234567890}}
user_preferences = {}

def get_user_currency(user_id):
    """
    Mendapatkan preferensi mata uang untuk pengguna.
    Mengembalikan kode mata uang atau mata uang default jika tidak diatur atau kedaluwarsa.
    """
    if user_id in user_preferences:
        # Memeriksa apakah preferensi telah kedaluwarsa
        timestamp = user_preferences[user_id]["timestamp"]
        current_time = time.time()
        
        # Jika preferensi masih berlaku
        if current_time - timestamp < USER_CURRENCY_TIMEOUT:
            return user_preferences[user_id]["currency"]
        else:
            # Preferensi kedaluwarsa, hapus
            del user_preferences[user_id]
    
    # Kembalikan mata uang default jika tidak ada preferensi atau kedaluwarsa
    return DEFAULT_CURRENCY

def set_user_currency(user_id, currency):
    """
    Mengatur preferensi mata uang untuk pengguna.
    """
    user_preferences[user_id] = {
        "currency": currency.upper(),
        "timestamp": time.time()
    }
    return user_preferences[user_id]["currency"]

def format_expiry_time(user_id):
    """
    Format waktu kapan preferensi mata uang akan kedaluwarsa.
    """
    if user_id not in user_preferences:
        return None
    
    timestamp = user_preferences[user_id]["timestamp"]
    expiry_time = timestamp + USER_CURRENCY_TIMEOUT
    expiry_datetime = datetime.fromtimestamp(expiry_time)
    
    return expiry_datetime.strftime("%H:%M:%S")

def clean_expired_preferences():
    """
    Menghapus preferensi pengguna yang kedaluwarsa.
    Panggil ini secara berkala untuk membersihkan.
    """
    current_time = time.time()
    expired_users = []
    
    for user_id, prefs in user_preferences.items():
        if current_time - prefs["timestamp"] >= USER_CURRENCY_TIMEOUT:
            expired_users.append(user_id)
    
    for user_id in expired_users:
        del user_preferences[user_id]
    
    return len(expired_users)