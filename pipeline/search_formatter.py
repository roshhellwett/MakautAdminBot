import html
from core.constants import CATEGORY_ICONS, KEYWORDS

def _format_date_simple(value):
    if not value: return ""
    return value.strftime("%d %b %Y")

def format_search_ui(notifications):
    """Refined UI formatter for Search Bot results."""
    if not notifications:
        return "❌ <b>No notices found.</b>\nTry different keywords like 'BCA' or 'Exam'."

    header = f"🔍 <b>Search Results: Found {len(notifications)} Notices</b>\n\n"
    items = []
    
    for i, n in enumerate(notifications, 1):
        clean_title = html.escape(n.title)
        date_str = _format_date_simple(n.published_date)
        
        # Determine icon based on decoupled constants
        icon = "📌"
        for cat, keys in KEYWORDS.items():
            if any(k in clean_title.lower() for k in keys):
                icon = CATEGORY_ICONS.get(cat, "📌")
                break
        
        date_suffix = f" (<i>{date_str}</i>)" if date_str else ""
        items.append(f"{i}. {icon} <a href='{n.source_url}'>{clean_title}</a>{date_suffix}")

    footer = "\n\n<i>Supreme system monitoring 24/7.</i>"
    return header + "\n\n".join(items) + footer
    #@academictelebotbyroshhellwett