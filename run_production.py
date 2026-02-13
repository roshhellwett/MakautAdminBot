import asyncio
import logging
import sys
import signal
import os

# Ensure the project root is in the Python path
sys.path.append(os.getcwd())

from core.logger import setup_logger
from database.init_db import init_db
from bot.telegram_app import start_telegram
from pipeline.ingest_pipeline import start_pipeline
from search_bot.search_app import start_search_bot 
from admin_bot.admin_app import start_admin_bot 
from group_bot.group_app import start_group_bot
from core.task_manager import supervised_task
from health_check import verify_system
from core.config import SEARCH_BOT_TOKEN, ADMIN_BOT_TOKEN

setup_logger()
logger = logging.getLogger("ORCHESTRATOR")

async def shutdown(signal, loop):
    """Graceful Shutdown for Railway Updates"""
    logger.info(f"🛑 Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def production_sequence():
    logger.info("🚀 ZENITH SUPREME: CLOUD BOOT SEQUENCE INITIALIZED")

    # PHASE 1: INFRASTRUCTURE
    try:
        await init_db()
        await verify_system()
    except Exception as e:
        logger.critical(f"💀 FATAL BOOT FAILURE: {e}")
        sys.exit(1)

    # PHASE 2: NETWORK CORE
    try:
        await start_telegram()
    except Exception as e:
        logger.critical(f"💀 TELEGRAM START FAILURE: {e}")
        sys.exit(1)

    # PHASE 3: SIGNAL HANDLERS
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s, loop)))

    # PHASE 4: CLUSTER LAUNCH
    tasks = [
        asyncio.create_task(supervised_task("SEARCH_BOT", start_search_bot)),
        asyncio.create_task(supervised_task("GROUP_BOT", start_group_bot)),
        asyncio.create_task(supervised_task("PIPELINE", start_pipeline))
    ]
    
    # SAFETY: Only launch Admin Bot if it has a UNIQUE token
    if ADMIN_BOT_TOKEN and ADMIN_BOT_TOKEN != SEARCH_BOT_TOKEN:
        tasks.append(asyncio.create_task(supervised_task("ADMIN_BOT", start_admin_bot)))
    else:
        logger.warning("⚠️ ADMIN BOT DISABLED: Token is missing or identical to Search Bot.")

    logger.info("✅ ALL SYSTEMS OPERATIONAL. MONITORING ACTIVE.")
    
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.info("👋 System Shutdown Complete.")

if __name__ == "__main__":
    try:
        asyncio.run(production_sequence())
    except KeyboardInterrupt:
        pass
        #@academictelebotbyroshhellwett