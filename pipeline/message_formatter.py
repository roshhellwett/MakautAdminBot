import html
from core.constants import CATEGORY_ICONS, KEYWORDS

def get_category_icon(title):
    """Assigns an icon based on the notice title using centralized keywords."""
    t = title.lower()
    for category, triggers in KEYWORDS.items():
        if any(k in t for k in triggers):
            return CATEGORY_ICONS.get(category, "📌")
    return CATEGORY_ICONS["DEFAULT"]

def format_message(item):
    """Formats a single notice for the Telegram Channel."""
    # Escape HTML special characters to prevent Telegram 'Bad Request' errors
    title = html.escape(item.get("title", "No Title"))
    url = item.get("source_url", "#")
    source = html.escape(item.get("source", "MAKAUT"))
    is_pdf = item.get("pdf_url") is not None
    
    icon = get_category_icon(title)
    header = f"{icon} <b>{source}</b>"
    
    if icon == "🚨":
        header = f"🚨 <b>URGENT {source} NOTICE</b>"

    link_text = "📄 Download PDF" if is_pdf else "🔗 Open Link"
    
    return (
        f"{header}\n\n"
        f"<b>{title}</b>\n\n"
        f"<a href='{url}'>{link_text}</a>"
    )