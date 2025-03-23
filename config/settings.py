import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Steam API settings
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
STEAM_STORE_API_URL = "https://store.steampowered.com/api/storesearch/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails/"
STEAMDB_CHARTS_URL = "https://steamdb.info/app/"

# Discord bot settings
COMMAND_PREFIX = "!search"
CURRENCY_PREFIX = "!currency"
BOT_TIMEOUT = 120  # Timeout for interactive components in seconds
USER_CURRENCY_TIMEOUT = 3600

DEFAULT_CURRENCY = "US"

CURRENCY_SYMBOLS = {
    "US": "$",
    "AR": "ARS$",
    "AU": "A$",
    "BR": "R$",
    "CA": "C$",
    "CL": "CLP$",
    "CN": "¥",
    "CO": "COL$",
    "CR": "₡",
    "EU": "€",
    "GB": "£",
    "HK": "HK$",
    "ID": "Rp",
    "IL": "₪",
    "IN": "₹",
    "JP": "¥",
    "KR": "₩",
    "KZ": "₸",
    "MX": "Mex$",
    "MY": "RM",
    "NO": "kr",
    "NZ": "NZ$",
    "PE": "S/.",
    "PH": "₱",
    "PL": "zł",
    "QA": "QR",
    "RU": "₽",
    "SA": "SR",
    "SG": "S$",
    "TH": "฿",
    "TR": "₺",
    "TW": "NT$",
    "UA": "₴",
    "AE": "AED",
    "UY": "$U",
    "VN": "₫",
    "ZA": "R",
}

SUPPORTED_CURRENCIES = {
    "US": "USD (United States Dollar)",
    "AR": "ARS (Argentine Peso)",
    "AU": "AUD (Australian Dollar)",
    "BR": "BRL (Brazilian Real)",
    "CA": "CAD (Canadian Dollar)",
    "CL": "CLP (Chilean Peso)",
    "CN": "CNY (Chinese Yuan)",
    "CO": "COP (Colombian Peso)",
    "CR": "CRC (Costa Rican Colón)",
    "EU": "EUR (Euro)",
    "GB": "GBP (British Pound)",
    "HK": "HKD (Hong Kong Dollar)",
    "ID": "IDR (Indonesian Rupiah)",
    "IL": "ILS (Israeli New Shekel)",
    "IN": "INR (Indian Rupee)",
    "JP": "JPY (Japanese Yen)",
    "KR": "KRW (South Korean Won)",
    "KZ": "KZT (Kazakhstani Tenge)",
    "MX": "MXN (Mexican Peso)",
    "MY": "MYR (Malaysian Ringgit)",
    "NO": "NOK (Norwegian Krone)",
    "NZ": "NZD (New Zealand Dollar)",
    "PE": "PEN (Peruvian Sol)",
    "PH": "PHP (Philippine Peso)",
    "PL": "PLN (Polish Złoty)",
    "QA": "QAR (Qatari Riyal)",
    "RU": "RUB (Russian Ruble)",
    "SA": "SAR (Saudi Riyal)",
    "SG": "SGD (Singapore Dollar)",
    "TH": "THB (Thai Baht)",
    "TR": "TRY (Turkish Lira)",
    "TW": "TWD (New Taiwan Dollar)",
    "UA": "UAH (Ukrainian Hryvnia)",
    "AE": "AED (United Arab Emirates Dirham)",
    "UY": "UYU (Uruguayan Peso)",
    "VN": "VND (Vietnamese Đồng)",
    "ZA": "ZAR (South African Rand)",
}