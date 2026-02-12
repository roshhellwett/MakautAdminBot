import asyncio
import logging
from telegram.error import RetryAfter, TimedOut, NetworkError
from bot.telegram_app import get_bot
from core.config import CHANNEL_ID

logger = logging.getLogger("CHANNEL_BROADCAST")

# Dynamic rate limiting: Stay safely under Telegram's 20 msg/min limit
BASE_DELAY = 3.5  
MAX_RETRIES = 5

async def broadcast_channel(messages):
    """Deliver messages with adaptive retries and session protection."""
    bot = get_bot()
    if not messages:
        return

    sent_count = 0
    for msg in messages:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg,
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                    read_timeout=20,
                    write_timeout=20
                )
                sent_count += 1
                await asyncio.sleep(BASE_DELAY) 
                break 

            except RetryAfter as e:
                logger.warning(f"⏳ Rate Limit hit: Waiting {e.retry_after}s...")
                await asyncio.sleep(e.retry_after + 1)

            except (TimedOut, NetworkError) as e:
                retries += 1
                logger.warning(f"📡 Network retry {retries}/{MAX_RETRIES}...")
                await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"❌ Critical Broadcast Error: {e}")
                break 

    if sent_count > 0:
        logger.info(f"📢 BATCH COMPLETE: {sent_count} notices broadcasted.")