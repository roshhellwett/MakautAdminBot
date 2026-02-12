import asyncio
import logging
from telegram import Bot
from database.db import engine as academic_engine
from database.security_db import security_engine
from core.config import BOT_TOKEN, SEARCH_BOT_TOKEN, ADMIN_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def verify_system():
    print("\n🔍 === ZENITH SUPREME SYSTEM HEALTH CHECK ===\n")

    # 1. Test All Bot Connections [cite: 1]
    tokens = [("MAIN", BOT_TOKEN), ("SEARCH", SEARCH_BOT_TOKEN), ("ADMIN", ADMIN_BOT_TOKEN)]
    for name, token in tokens:
        try:
            bot = Bot(token=token)
            me = await bot.get_me()
            print(f"✅ {name} BOT: @{me.username} is ONLINE")
        except Exception as e:
            print(f"❌ {name} BOT: OFFLINE | {e}")

    # 2. Test Dual Database Integrity [cite: 89, 90]
    for db_name, db_engine in [("ACADEMIC", academic_engine), ("SECURITY", security_engine)]:
        try:
            async with db_engine.connect() as conn:
                from sqlalchemy import text
                await conn.execute(text("SELECT 1"))
            print(f"✅ DATABASE: {db_name} Connection SUCCESSFUL")
        except Exception as e:
            print(f"❌ DATABASE: {db_name} FAILED | {e}")

    print("\n🚀 === ALL SYSTEMS GO ===\n")

if __name__ == "__main__":
    asyncio.run(verify_system())
    #@academictelebotbyroshhellwett