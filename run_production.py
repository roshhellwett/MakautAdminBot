import asyncio
import logging
from core.task_manager import supervised_task
from zenith_group_bot.group_app import start_group_bot
from core.logger import setup_logger

setup_logger()

async def main():
    logging.info("🚀 ZENITH SUPREME EDITION: CLUSTER START")
    await asyncio.gather(
        supervised_task("GROUP_MONITOR", start_group_bot)
    )

if __name__ == "__main__":
    asyncio.run(main())