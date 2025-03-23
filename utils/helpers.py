import re
from config.settings import CURRENCY_SYMBOLS
from utils.user_prefs import get_user_currency

def sanitize_html(html_text):
    """Menghilangkan tag HTML dari teks."""
    if not html_text:
        return ""
    
    # Menghapus tag HTML
    clean_text = re.sub(r'<[^>]*>', '', html_text)
    
    # Mengganti entitas HTML
    clean_text = clean_text.replace('&amp;', '&')
    clean_text = clean_text.replace('&lt;', '<')
    clean_text = clean_text.replace('&gt;', '>')
    clean_text = clean_text.replace('&quot;', '"')
    clean_text = clean_text.replace('&nbsp;', ' ')
    
    return clean_text.strip()

def format_price(price_in_cents, user_id=None):
    """Format harga dengan format mata uang yang sesuai."""
    if price_in_cents == 0:
        return "Gratis"

    currency_code = get_user_currency(user_id)
    symbol = CURRENCY_SYMBOLS.get(currency_code, "$")
    
    price = price_in_cents / 100

    if currency_code in ["JP", "KR", "VN", "ID"]:
        price_formatted = f"{symbol}{int(price):,}"
        if currency_code == "ID":
            price_formatted = price_formatted.replace(",", ".")
    else:
        price_formatted = f"{symbol}{price:.2f}"

    return price_formatted

def truncate_text(text, max_length=200, add_ellipsis=True):
    """Memotong teks menjadi panjang maksimum tertentu."""
    if not text or len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    if add_ellipsis:
        truncated += "..."
    
    return truncated