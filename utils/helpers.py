import re

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

def format_price(price_in_cents):
    """Format price from cents to dollars with proper formatting."""
    if price_in_cents == 0:
        return "Free to Play"
    
    price = price_in_cents / 100
    return f"${price:.2f}"

def truncate_text(text, max_length=200, add_ellipsis=True):
    """Truncate text to a maximum length."""
    if not text or len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    if add_ellipsis:
        truncated += "..."
    
    return truncated