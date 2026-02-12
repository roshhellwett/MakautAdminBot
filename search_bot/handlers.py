import logging
from database.repository import NotificationRepo
from pipeline.search_formatter import format_search_ui

logger = logging.getLogger("SEARCH_HANDLERS")

async def get_latest_results(limit: int = 10):
    """
    Fetches recent notices using the decoupled Repository pattern.
    """
    try:
        # 1. Fetch Data via Repo (No SQL here)
        notices = await NotificationRepo.get_latest(limit)
        
        # 2. Format UI using dedicated Search Formatter
        return format_search_ui(notices)

    except Exception as e:
        logger.error(f"Handler Error (Latest): {e}")
        return "❌ <b>System Error:</b> Could not retrieve data at this time."

async def search_by_keyword(query: str, limit: int = 10):
    """
    Executes keyword search using the decoupled Repository pattern.
    """
    # Basic validation
    if not query or len(query.strip()) < 2:
        return "⚠️ <b>Search too short.</b>\nPlease enter at least 2 characters."

    try:
        # 1. Fetch Data via Repo (No SQL here)
        results = await NotificationRepo.search_query(query.strip(), limit)
        
        # 2. Format UI
        if not results:
            return f"🔍 No notices found matching: <b>{query}</b>"
            
        return format_search_ui(results)

    except Exception as e:
        logger.error(f"Handler Error (Search - {query}): {e}")
        return "❌ <b>System Error:</b> Search service is temporarily unavailable."
        #@academictelebotbyroshhellwett