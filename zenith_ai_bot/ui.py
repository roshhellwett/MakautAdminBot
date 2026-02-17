from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core.config import ADMIN_USER_ID


def get_ai_dashboard(is_pro: bool, persona: str, usage: dict) -> InlineKeyboardMarkup:
    persona_label = persona.capitalize() if persona != "default" else "Default"
    rows = [
        [InlineKeyboardButton(f"{'💎' if is_pro else '🆓'} {'PRO ACTIVE' if is_pro else 'FREE TIER'}", callback_data="ai_status")],
        [
            InlineKeyboardButton(f"🎭 Persona: {persona_label}", callback_data="ai_personas"),
            InlineKeyboardButton("📊 Usage", callback_data="ai_usage"),
        ],
        [
            InlineKeyboardButton("🔬 Research", callback_data="ai_research_help"),
            InlineKeyboardButton("📝 Summarize", callback_data="ai_summarize_help"),
        ],
        [
            InlineKeyboardButton("💻 Code", callback_data="ai_code_help"),
            InlineKeyboardButton("🎨 Imagine", callback_data="ai_imagine_help"),
        ],
        [InlineKeyboardButton("💬 Chat History", callback_data="ai_history")],
    ]
    if not is_pro:
        rows.append([InlineKeyboardButton("💬 Buy Pro", url=f"tg://user?id={ADMIN_USER_ID}")])
    return InlineKeyboardMarkup(rows)


def get_persona_keyboard(current: str) -> InlineKeyboardMarkup:
    personas = [
        ("🤖 Default", "default"),
        ("💻 Coder", "coder"),
        ("✍️ Writer", "writer"),
        ("📊 Analyst", "analyst"),
        ("🎓 Tutor", "tutor"),
        ("⚔️ Debate", "debate"),
        ("🔥 Roast", "roast"),
    ]
    rows = []
    for label, key in personas:
        marker = " ✅" if key == current else ""
        rows.append([InlineKeyboardButton(f"{label}{marker}", callback_data=f"ai_persona_{key}")])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="ai_main_menu")])
    return InlineKeyboardMarkup(rows)


def get_back_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Terminal", callback_data="ai_main_menu")]])


def get_history_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑️ Clear History", callback_data="ai_clear_history")],
        [InlineKeyboardButton("🔙 Back", callback_data="ai_main_menu")],
    ])
