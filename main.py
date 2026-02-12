import asyncio
import logging
import sys

from core.logger import setup_logger
from database.init_db import init_db
from bot.telegram_app import start_telegram, get_bot
from pipeline.ingest_pipeline import start_pipeline
from search_bot.search_app import start_search_bot 
from admin_bot.admin_app import start_admin_bot 
from group_bot.group_app import start_group_bot
from core.task_manager import supervised_task
from core.config import ADMIN_ID

setup_logger()
logger = logging.getLogger("MAIN")

async def main():
    logger.info("🚀 ACADEMIC TELE-BOT: ZENITH SUPREME INITIALIZING")

    # 1. Database & Broadcast Core
    try:
        await init_db()
        await start_telegram()
    except Exception as e:
        logger.critical(f"🛑 BOOTSTRAP FATAL: {e}")
        return

    # 2. Sequential Staggered Deployment (20s Gaps)
    logger.info("📡 CLUSTER STARTING: Sequential staggered deployment...")
    
    # We use the decoupled task manager for supervision
    tasks = []
    
    tasks.append(asyncio.create_task(supervised_task("SEARCH_BOT", start_search_bot)))
    await asyncio.sleep(20)
    
    tasks.append(asyncio.create_task(supervised_task("ADMIN_BOT", start_admin_bot)))
    await asyncio.sleep(20)
    
    tasks.append(asyncio.create_task(supervised_task("GROUP_BOT", start_group_bot)))
    await asyncio.sleep(20)
    
    tasks.append(asyncio.create_task(supervised_task("INGEST_PIPELINE", start_pipeline)))

    # Health Check Notification
    if ADMIN_ID != 0:
        try:
            await get_bot().send_message(ADMIN_ID, "✅ <b>System Online:</b> Architecture Decoupled & Active.", parse_mode="HTML")
        except: pass

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ SHUTDOWN: System stopped.")
        sys.exit(0)