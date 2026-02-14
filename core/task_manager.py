import asyncio
import logging

logger = logging.getLogger("TASK_MANAGER")
active_services = set()

async def supervised_task(name, coro_func):
    """Zenith Supreme: Automatic Recovery Supervisor."""
    if name in active_services: return
    active_services.add(name)
    
    retry_delay = 5
    while True:
        try:
            logger.info(f"🔄 [DEPLOYING] {name}...")
            await coro_func()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"❌ {name} CRITICAL FAILURE: {e}. Restarting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)