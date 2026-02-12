import re
import asyncio
import unicodedata
from group_bot.word_list import BANNED_WORDS, SPAM_DOMAINS

# UPGRADE: Pre-compile pattern once at startup for maximum speed
ABUSE_PATTERN = re.compile(r"(?i)\b(" + "|".join(re.escape(word) for word in BANNED_WORDS) + r")\b")

def _run_regex_sync(text):
    """Zenith Deep Scan Engine: Optimized with pre-compiled patterns."""
    if not text:
        return False, None

    # Unicode Normalization
    normalized_text = unicodedata.normalize("NFKD", text).lower() [cite: 52]
    
    # De-Noising: Remove all symbols and spaces
    noise_free = re.sub(r'[^a-zA-Z0-9\u0900-\u097F\u0980-\u09FF\s]', '', normalized_text) [cite: 52]
    collapsed_text = noise_free.replace(" ", "") [cite: 52]

    # Optimized Forensic Match
    if ABUSE_PATTERN.search(collapsed_text):
        return True, "Abusive/Inappropriate Language"

    # Smart Link Protection
    if "makaut" not in normalized_text: [cite: 53]
        for domain in SPAM_DOMAINS: [cite: 53]
            if domain in normalized_text: [cite: 53]
                return True, "Unauthorized/Suspicious Link" [cite: 53]

    return False, None

async def is_inappropriate(text: str) -> (bool, str):
    if not text:
        return False, None
    return await asyncio.to_thread(_run_regex_sync, text)
#@academictelebotbyroshhellwett