import logging
from telegram import Update
from telegram.ext import ContextTypes
from zenith_group_bot.repository import GroupRepo

logger = logging.getLogger("VIOLATION_TRACKER")

async def handle_violation(update: Update, context: ContextTypes.DEFAULT_TYPE, reason: str):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    
    try:
        await update.message.delete()
    except Exception as e:
        logger.error(f"Could not delete message: {e}")
        
    strikes = await GroupRepo.process_violation(user_id, chat_id)
    
    if strikes >= 3:
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.send_message(
                chat_id, 
                f"🚨 <b>BANNED:</b> {user_name} has been removed for repeated violations ({reason}).",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Could not ban user: {e}")
    else:
        warning = await context.bot.send_message(
            chat_id,
            f"⚠️ <b>WARNING ({strikes}/3):</b> {user_name}, your message was removed ({reason}).",
            parse_mode="HTML"
        )