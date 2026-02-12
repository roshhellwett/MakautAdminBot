import asyncio
import logging
import telegram.error

logger = logging.getLogger("TASK_MANAGER")

# Global lock to prevent race-condition duplicate starts
active_services = set()

async def supervised_task(name, coro_func):
    """
    Shielded task runner with automatic Conflict-Shield and exponential backoff.
    Ensures 24/7 uptime by catching crashes and restarting services.
    """
    if name in active_services:
        logger.warning(f"⚠️ {name} is already active. Skipping duplicate start.")
        return
    
    active_services.add(name)
    retry_delay = 15 

    while True:
        try:
            logger.info(f"🔄 [DEPLOYING] {name}...")
            await coro_func()
            # If coro_func returns naturally, the service has stopped intentionally
            active_services.discard(name)
            break 
        except telegram.error.Conflict:
            logger.error(f"💥 {name} CONFLICT: Session collision. Cooling down for 60s...")
            await asyncio.sleep(60) 
        except asyncio.CancelledError:
            logger.info(f"🛑 {name} Stopped by System.")
            break
        except Exception as e:
            logger.error(f"❌ {name} CRITICAL FAILURE: {e}. Restarting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 120)