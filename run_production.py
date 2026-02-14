import asyncio
import logging
from core.task_manager import supervised_task
from zenith_group_bot.group_app import start_group_bot

# ==========================================
# 1. BASE LOGGING CONFIGURATION
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ==========================================
# 2. SILENCE THE NETWORK SPAM
# ==========================================
# This stops httpx from printing "HTTP Request: POST..." every 2 seconds
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

async def main():
    logging.info("🚀 ZENITH SUPREME EDITION: CLUSTER START")
    
    # Launch the supervisor engine which manages the Group Bot microservice
    await asyncio.gather(
        supervised_task("GROUP_MONITOR", start_group_bot)
    )

if __name__ == "__main__":
    # Start the asyncio event loop
    asyncio.run(main())