import asyncio
from typing import Callable, Coroutine, Any
from core.logger import setup_logger

logger = setup_logger("TASK_MANAGER")
active_services = set()
# 🚀 PREVENT GC FROM KILLING BACKGROUND TASKS
background_tasks = set()

def fire_and_forget(coro: Coroutine[Any, Any, Any]) -> None:
    """Safely executes background tasks without blocking and prevents GC."""
    task = asyncio.create_task(coro)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

async def supervised_task(name: str, coro_func: Callable[[], Coroutine[Any, Any, Any]]):
    if name in active_services: return
    active_services.add(name)
    retry_delay = 5
    while True:
        try:
            logger.info(f"🔄 [DEPLOYING] {name}...")
            await coro_func()
        except asyncio.CancelledError:
            logger.info(f"🛑 [SHUTDOWN] {name} task cancelled gracefully.")
            break
        except Exception as e:
            logger.error(f"❌ {name} CRITICAL FAILURE: {e}. Restarting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)