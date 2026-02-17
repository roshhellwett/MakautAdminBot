from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_dashboard(is_pro: bool = False):
    """The clean, institutional dashboard for all users."""
    status_text = "🟢 PRO: ACTIVE" if is_pro else "🔒 UPGRADE TO PRO"
    radar_text = "⚡ Live Orderflow (Pro)" if is_pro else "📊 Live Orderflow (Standard)"
    
    keyboard = [
        [InlineKeyboardButton(radar_text, callback_data="ui_whale_radar")],
        [InlineKeyboardButton("🔍 Deep-Scan Audit", callback_data="ui_audit"),
         InlineKeyboardButton("🗂️ Audit Vault", callback_data="ui_saved_audits")],
        [InlineKeyboardButton("📈 Smart Money Pulse", callback_data="ui_volume")],
        [InlineKeyboardButton(status_text, callback_data="ui_pro_info")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_audits_keyboard(audits):
    """Generates the interactive history list allowing specific deletions."""
    keyboard = []
    
    for a in audits:
        short_contract = f"{a.contract[:6]}...{a.contract[-4:]}"
        keyboard.append([
            InlineKeyboardButton(f"📜 View: {short_contract}", callback_data=f"ui_view_audit_{a.id}"),
            InlineKeyboardButton("🗑️ Delete", callback_data=f"ui_del_audit_{a.id}")
        ])
    
    if audits:
        keyboard.append([InlineKeyboardButton("🚨 Wipe Entire Vault", callback_data="ui_clear_audits")])
        
    keyboard.append([InlineKeyboardButton("🔙 Return to Terminal", callback_data="ui_main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Return to Terminal", callback_data="ui_main_menu")]])

def get_welcome_msg(name: str):
    return (
        f"<b>AUTHENTICATED: Welcome to Zenith, {name}.</b>\n\n"
        "97% of retail traders act as exit liquidity for institutional algorithms. Zenith is designed to flip that statistical disadvantage. We monitor raw mempool data to detect where 'Smart Money' is moving before the market reacts.\n\n"
        "<b>📊 STANDARD ACCESS (Free)</b>\n"
        "You have delayed access to mid-tier on-chain volume. Contract hashes, specific liquidity metrics, and actionable trading links are restricted.\n\n"
        "<b>⚡ PRO ACCESS (Zero-Latency)</b>\n"
        "Unrestricted access to $1M+ capital routing, unredacted smart contract decompilation, and instant DEX execution routing.\n\n"
        "<i>Select a module below to initialize your terminal.</i>"
    )