import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==============================
# TELEGRAM TOKENS
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
SEARCH_BOT_TOKEN = os.getenv("SEARCH_BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GROUP_BOT_TOKEN = os.getenv("GROUP_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Critical Check: System cannot run without the main bot token
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing in .env")

# ==============================
# DATABASE CONFIGURATION
# ==============================
# Forced async driver for SQLAlchemy 2.0 compatibility [cite: 84]
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///makaut.db")

# ==============================
# PIPELINE & LOGIC 
# ==============================
SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", "300"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
TARGET_YEAR = 2025  # Centralized Gatekeeper Year [cite: 31, 34]

# FIXED: Added missing LOG_LEVEL with a safe default 
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==============================
# SECURITY & NETWORK
# ==============================
# SSL Safety: Targeted exemptions for known legacy university certs [cite: 36, 44]
SSL_VERIFY_EXEMPT = ["makautexam.net", "www.makautexam.net"]
REQUEST_TIMEOUT = 30.0  # Prevents hanging on slow university servers
MAX_PDF_SIZE_MB = 10    # Memory guard to prevent OOM crashes [cite: 45]
#@academictelebotbyroshhellwett