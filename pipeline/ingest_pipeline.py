import asyncio
import logging
from scraper.makaut_scraper import scrape_source
from core.sources import URLS
from database.repository import NotificationRepo
from delivery.channel_broadcaster import broadcast_channel
from pipeline.message_formatter import format_message
from core.config import SCRAPE_INTERVAL

logger = logging.getLogger("PIPELINE")

async def start_pipeline():
    logger.info("🚀 SUPREME ASYNC PIPELINE: ACTIVATED")
    while True:
        cycle_start = asyncio.get_event_loop().time()
        
        for key, config in URLS.items():
            try:
                # Task Isolation: One source failing doesn't stop the loop
                items = await scrape_source(key, config)
                if not items: continue

                new_notices = []
                for item in items:
                    # REPO PATTERN: Delegating DB logic to the DAL
                    is_new = await NotificationRepo.add_notification(item)
                    if is_new:
                        new_notices.append(format_message(item))
                
                # Broadcast only new items
                if new_notices:
                    await broadcast_channel(new_notices)
                
                await asyncio.sleep(2) # Backpressure protection
            except Exception as e:
                logger.error(f"Pipeline Error in {key}: {e}")

        # Dynamic Heartbeat
        elapsed = asyncio.get_event_loop().time() - cycle_start
        await asyncio.sleep(max(10, SCRAPE_INTERVAL - elapsed))
        #@academictelebotbyroshhellwett