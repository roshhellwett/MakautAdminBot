import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# TELEGRAM
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
SEARCH_BOT_TOKEN = os.getenv("SEARCH_BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing in .env")

# ==============================
# DATABASE
# ==============================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///makaut.db"

# ==============================
# PIPELINE & ADMIN
# ==============================
try:
    SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", "300"))
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
except ValueError:
    SCRAPE_INTERVAL = 300
    ADMIN_ID = 0

# ==============================
# GEMINI API KEY (Single Key Logic)
# ==============================
# Ensure this matches exactly what pdf_processor.py expects to import
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") 
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")