from datetime import datetime, timedelta
import pytz

IST = pytz.timezone('Asia/Kolkata')

def get_now_ist():
    """Returns the current time in IST."""
    return datetime.now(IST)

def format_for_telegram(dt):
    """Standardizes date formatting for all bot messages."""
    if not dt:
        return "Unknown Date"
    return dt.strftime("%d %b %Y | %I:%M %p IST")