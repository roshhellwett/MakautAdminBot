import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from core.config import GROUP_BOT_TOKEN
from zenith_group_bot.repository import init_group_db
from zenith_group_bot.filters import contains_profanity_or_spam
from zenith_group_bot.flood_control import is_flooding
from zenith_group_bot.violation_tracker import handle_violation

logger = logging.getLogger("GROUP_BOT")

async def monitor_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
        
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text
    
    if contains_profanity_or_spam(text):
        await handle_violation(update, context, "Banned Content")
        return
        
    if is_flooding(user_id, chat_id):
        await handle_violation(update, context, "Message Flooding")
        return

async def start_group_bot():
    logger.info("Initializing Database...")
    await init_group_db()
    
    app = ApplicationBuilder().token(GROUP_BOT_TOKEN).build()
    
    # Generic Monitor: Listens to ALL groups simultaneously
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, monitor_messages))
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()