import re
from config.settings import CURRENCY_SYMBOLS
from utils.user_prefs import get_user_currency

def sanitize_html(html_text):
    """Remove HTML tags from text."""
    if not html_text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]*>', '', html_text)
    
    # Replace HTML entities
    clean_text = clean_text.replace('&amp;', '&')
    clean_text = clean_text.replace('&lt;', '<')
    clean_text = clean_text.replace('&gt;', '>')
    clean_text = clean_text.replace('&quot;', '"')
    clean_text = clean_text.replace('&nbsp;', ' ')
    
    return clean_text.strip()

def format_price(price_in_cents, user_id=None):
    """Format price from cents to dollars with proper formatting."""
    if price_in_cents == 0:
        return "Free to Play"

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
    """Truncate text to a maximum length."""
    if not text or len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    if add_ellipsis:
        truncated += "..."
    
    return truncated