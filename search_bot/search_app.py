import os
import logging
import asyncio
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from search_bot.handlers import get_latest_results, search_by_keyword
from group_bot.flood_control import is_flooding

logger = logging.getLogger("SEARCH_BOT")

# Filter UI Configuration
FAST_FILTERS = [["/latest", "BCA", "CSE"], ["Exam", "Result", "Form"]]

async def start_search_bot():
    token = os.getenv("SEARCH_BOT_TOKEN")
    if not token:
        logger.error("SEARCH_BOT_TOKEN missing!")
        return

    # Build app with hardened timeouts for stability
    app = ApplicationBuilder().token(token).read_timeout(30).connect_timeout(30).build()
    reply_markup = ReplyKeyboardMarkup(FAST_FILTERS, resize_keyboard=True)
    
    async def start_cmd(update, context):
        await update.message.reply_text(
            "🔍 <b>Supreme Search Mode</b>\nSend a keyword or use the filters below.",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    async def latest_cmd(update, context):
        user_id = update.effective_user.id
        
        # SPAM SHIELD: Frequency check using global flood control logic
        flooding, reason = is_flooding(user_id, "/latest")
        if flooding:
            await update.message.reply_text(f"⚠️ <b>Slow down!</b> {reason}")
            return

        result_text = await get_latest_results()
        await update.message.reply_text(result_text, parse_mode="HTML", disable_web_page_preview=True)

    async def handle_msg(update, context):
        if not update.message or not update.message.text: 
            return
        
        query = update.message.text
        user_id = update.effective_user.id
        
        # SPAM SHIELD: Content & Frequency check
        flooding, reason = is_flooding(user_id, query)
        if flooding:
            # Block the request and warn the user
            await update.message.reply_text(f"🛑 <b>Access Restricted:</b> {reason}")
            return

        result_text = await search_by_keyword(query)
        await update.message.reply_text(result_text, parse_mode="HTML", disable_web_page_preview=True)

    # Register Handlers
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("latest", latest_cmd))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    logger.info("SEARCH BOT GOD MODE ACTIVE WITH SPAM SHIELD")
    
    # CRITICAL FIX: Keep this coroutine alive forever so the task doesn't finish
    await asyncio.Event().wait()