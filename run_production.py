import asyncio
import logging
import sys
import os

# Ensure the project root is in the Python path
sys.path.append(os.getcwd())

from core.logger import setup_logger
from core.task_manager import supervised_task
from core.config import ADMIN_ID

# Infrastructure Imports
from database.init_db import init_db
from health_check import verify_system
from bot.telegram_app import start_telegram, get_bot

# Service Imports
from search_bot.search_app import start_search_bot
from admin_bot.admin_app import start_admin_bot
from group_bot.group_app import start_group_bot
from pipeline.ingest_pipeline import start_pipeline

setup_logger()
logger = logging.getLogger("ORCHESTRATOR")

async def production_sequence():
    print("""
    ░░█ █▀▀ █▄░█ █ ▀█▀ █░█   █▀ █░█ █▀█ █▀█ █▀▀ █▀▄▀█ █▀▀
    █▄█ ██▄ █░▀█ █ ░█░ █▀█   ▄█ █▄█ █▀▀ █▀▄ ██▄ █░▀░█ ██▄
    >>> ACADEMIC TELE-BOT PRODUCTION ENGINE STARTING...
    """)

    # PHASE 1: INFRASTRUCTURE VALIDATION
    logger.info("🛠️ PHASE 1: Infrastructure Initialization...")
    
    try:
        # 1. Initialize Databases (Academic + Security)
        await init_db()
        
        # 2. Run Pre-Flight Health Check
        logger.info("🩺 Running System Health Check...")
        await verify_system()
        
    except Exception as e:
        logger.critical(f"🛑 BOOTSTRAP FAILED: {e}")
        sys.exit(1)

    # PHASE 2: NETWORK CORE START
    logger.info("📡 PHASE 2: Establishing Network Core...")
    try:
        await start_telegram()
        logger.info("✅ Main Broadcast Bot: ONLINE")
    except Exception as e:
        logger.critical(f"🛑 NETWORK FAILED: {e}")
        sys.exit(1)

    # PHASE 3: STAGGERED CLUSTER DEPLOYMENT
    logger.info("🚀 PHASE 3: Deploying Service Cluster (Staggered Mode)...")
    
    tasks = []

    # Service 1: Search Bot (High Availability)
    logger.info("   >>> Launching Search Bot...")
    tasks.append(asyncio.create_task(supervised_task("SEARCH_BOT", start_search_bot)))
    await asyncio.sleep(20) # Conflict Prevention Gap

    # Service 2: Admin Bot (Control Plane)
    logger.info("   >>> Launching Admin Bot...")
    tasks.append(asyncio.create_task(supervised_task("ADMIN_BOT", start_admin_bot)))
    await asyncio.sleep(20)

    # Service 3: Group Bot (Moderation & Defense)
    logger.info("   >>> Launching Group Bot...")
    tasks.append(asyncio.create_task(supervised_task("GROUP_BOT", start_group_bot)))
    await asyncio.sleep(20)

    # Service 4: Ingest Pipeline (Data Acquisition)
    logger.info("   >>> Launching Ingest Pipeline...")
    tasks.append(asyncio.create_task(supervised_task("INGEST_PIPELINE", start_pipeline)))

    # PHASE 4: CONFIRMATION
    if ADMIN_ID != 0:
        try:
            await get_bot().send_message(
                chat_id=ADMIN_ID, 
                text="🚀 <b>Zenith Production Online</b>\nAll systems nominal.\nArchitecture: Decoupled/Async",
                parse_mode="HTML"
            )
        except Exception:
            logger.warning("⚠️ Could not send Admin confirmation.")

    logger.info("✅ ALL SYSTEMS GO. MONITORING ACTIVE.")
    
    # Keep the event loop alive forever
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        # FIXED: Removed WindowsSelectorEventLoopPolicy to allow Subprocess (git pull) support
        asyncio.run(production_sequence())
    except KeyboardInterrupt:
        logger.info("⏹️ SHUTDOWN: Production sequence stopped by user.")
        sys.exit(0)