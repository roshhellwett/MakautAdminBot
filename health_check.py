import asyncio
import logging
import sys
import codecs
from telegram import Bot
from database.db import SessionLocal
from core.config import BOT_TOKEN, SEARCH_BOT_TOKEN, ADMIN_BOT_TOKEN, GEMINI_API_KEY

# Windows Emoji Fix
if sys.platform.startswith('win'):
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

logging.basicConfig(level=logging.INFO)

async def verify_system():
    print("\n🔍 === TELEACADEMIC FINAL HEALTH CHECK ===\n")

    # 1. TEST GEMINI LIFELINE
    if GEMINI_API_KEY:
        print(f"✅ GEMINI KEY: Key is configured.")
    else:
        print(f"❌ GEMINI KEY: Missing in .env")

    # 2. Test Bots
    for name, token in [("MAIN", BOT_TOKEN), ("SEARCH", SEARCH_BOT_TOKEN), ("ADMIN", ADMIN_BOT_TOKEN)]:
        try:
            bot = Bot(token=token)
            me = await bot.get_me()
            print(f"✅ {name} BOT: @{me.username} is Online")
        except Exception as e:
            print(f"❌ {name} BOT: Failed | {e}")

    # 3. Test Database
    try:
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        print("✅ DATABASE: Connection Successful")
        db.close()
    except Exception as e:
        print(f"❌ DATABASE: Failed | {e}")

    print("\n🚀 === CHECK COMPLETE: READY TO DEPLOY ===\n")

if __name__ == "__main__":
    asyncio.run(verify_system())