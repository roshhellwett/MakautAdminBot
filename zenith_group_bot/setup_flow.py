import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.logger import setup_logger
from zenith_crypto_bot.repository import SubscriptionRepo
from zenith_group_bot.repository import SettingsRepo

logger = setup_logger("SETUP_FLOW")

setup_state = {}

FEATURES_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🛡️ Anti-Spam Only", callback_data="setup_feat_spam")],
    [InlineKeyboardButton("🚫 Anti-Abuse Only", callback_data="setup_feat_abuse")],
    [InlineKeyboardButton("⚔️ Both (Recommended)", callback_data="setup_feat_both")],
])

STRENGTH_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🟢 Low (5 strikes)", callback_data="setup_str_low")],
    [InlineKeyboardButton("🟡 Medium (3 strikes)", callback_data="setup_str_medium")],
    [InlineKeyboardButton("🔴 High (2 strikes)", callback_data="setup_str_high")],
])


async def cmd_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.chat.type not in ("group", "supergroup"):
        return await msg.reply_text(
            "⚠️ Add this bot to your group and use /setup in the group chat."
        )

    chat_id = msg.chat_id
    user_id = msg.from_user.id

    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        if member.status not in ("administrator", "creator"):
            return await msg.reply_text("⛔ Only group admins can run /setup.")
    except Exception:
        return await msg.reply_text("⚠️ Cannot verify admin status. Make sure I'm an admin.")

    is_pro = await SubscriptionRepo.is_pro(user_id)
    existing_groups = await SettingsRepo.count_owned_groups(user_id)

    existing_settings = await SettingsRepo.get_settings(chat_id)
    is_new_group = existing_settings is None or existing_settings.owner_id != user_id

    if is_new_group:
        max_groups = 5 if is_pro else 1
        if existing_groups >= max_groups:
            tier_msg = (
                f"⚠️ <b>Group limit reached</b>\n\n"
                f"You have <b>{existing_groups}/{max_groups}</b> active groups.\n\n"
            )
            if not is_pro:
                tier_msg += (
                    "💎 Upgrade to <b>Zenith Pro</b> for up to <b>5 groups</b>.\n"
                    "<code>/activate [YOUR_KEY]</code>"
                )
            else:
                tier_msg += "Pro limit: 5 groups. Use /reset in an old group to free up a slot."
            return await msg.reply_text(tier_msg, parse_mode="HTML")

    group_name = msg.chat.title or f"Group {chat_id}"

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"⚙️ <b>SETUP: {html.escape(group_name)}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"<b>Step 1/2:</b> Select protection features:"
            ),
            reply_markup=FEATURES_KEYBOARD,
            parse_mode="HTML",
        )
        setup_state[user_id] = {
            "chat_id": chat_id,
            "group_name": group_name,
            "step": "features",
        }
        await msg.reply_text("✅ Check your DMs — I sent the setup wizard!")
    except Exception:
        await msg.reply_text("⚠️ I can't DM you. Start a private chat with me first.")


async def setup_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in setup_state:
        return await query.edit_message_text("⚠️ Session expired. Run /setup again in your group.")

    data = query.data
    state = setup_state[user_id]

    if data.startswith("setup_feat_"):
        feature = data.replace("setup_feat_", "")
        state["features"] = feature
        state["step"] = "strength"
        await query.edit_message_text(
            f"⚙️ <b>SETUP: {html.escape(state['group_name'])}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✅ Features: <b>{feature.capitalize()}</b>\n\n"
            f"<b>Step 2/2:</b> Select enforcement strength:",
            reply_markup=STRENGTH_KEYBOARD,
            parse_mode="HTML",
        )

    elif data.startswith("setup_str_"):
        strength = data.replace("setup_str_", "")
        state["strength"] = strength

        try:
            record = await SettingsRepo.upsert_settings(
                chat_id=state["chat_id"],
                owner_id=user_id,
                group_name=state["group_name"],
                features=state["features"],
                strength=strength,
                is_active=True,
            )

            is_pro = await SubscriptionRepo.is_pro(user_id)
            pro_section = ""
            if is_pro:
                pro_section = (
                    "\n\n<b>💎 PRO COMMANDS:</b>\n"
                    "• <code>/addword [word]</code> — Custom word filter\n"
                    "• <code>/antiraid on/off</code> — Anti-raid lockdown\n"
                    "• <code>/analytics</code> — Moderation stats\n"
                    "• <code>/schedule HH:MM [msg]</code> — Scheduled messages\n"
                    "• <code>/welcome [msg]</code> — Custom welcome\n"
                    "• <code>/auditlog</code> — View audit log"
                )

            await query.edit_message_text(
                f"✅ <b>SETUP COMPLETE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"<b>Group:</b> {html.escape(state['group_name'])}\n"
                f"<b>Features:</b> {state['features'].capitalize()}\n"
                f"<b>Strength:</b> {strength.capitalize()}\n"
                f"<b>Status:</b> ✅ Active{pro_section}\n\n"
                f"<b>Core Commands:</b>\n"
                f"• <code>/forgive</code> — Clear user strikes\n"
                f"• <code>/reset</code> — Wipe group data\n"
                f"• <code>/setup</code> — Reconfigure",
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Setup save failed: {e}")
            await query.edit_message_text("❌ Setup failed. Please try again.")
        finally:
            setup_state.pop(user_id, None)