from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core.config import ADMIN_USER_ID


def get_admin_dashboard(is_pro: bool, groups: list) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(f"{'💎' if is_pro else '🆓'} {'PRO ACTIVE' if is_pro else 'FREE TIER'}", callback_data="grp_status")],
        [InlineKeyboardButton(f"📋 My Groups ({len(groups)})", callback_data="grp_list")],
    ]
    if is_pro:
        rows.extend([
            [
                InlineKeyboardButton("📊 Analytics", callback_data="grp_analytics_pick"),
                InlineKeyboardButton("📜 Audit Log", callback_data="grp_audit_pick"),
            ],
            [
                InlineKeyboardButton("📝 Custom Words", callback_data="grp_words_help"),
                InlineKeyboardButton("⏰ Schedules", callback_data="grp_schedule_help"),
            ],
            [InlineKeyboardButton("👋 Welcome", callback_data="grp_welcome_help")],
        ])
    else:
        rows.append([InlineKeyboardButton("💬 Buy Pro", url=f"tg://user?id={ADMIN_USER_ID}")])
    return InlineKeyboardMarkup(rows)


def get_group_picker(groups: list, action_prefix: str) -> InlineKeyboardMarkup:
    rows = []
    for g in groups[:5]:
        name = g.group_name or f"Group {g.chat_id}"
        status = "✅" if g.is_active else "⏸️"
        rows.append([InlineKeyboardButton(f"{status} {name}", callback_data=f"{action_prefix}_{g.chat_id}")])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="grp_main_menu")])
    return InlineKeyboardMarkup(rows)


def get_back_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="grp_main_menu")]])
