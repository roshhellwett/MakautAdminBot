import re
import asyncio
import unicodedata
from group_bot.word_list import BANNED_WORDS, SPAM_DOMAINS

# Pre-compile the pattern to find banned words anywhere in a sentence
# This matches the word even if surrounded by other text
# Using \b word boundaries for the first pass to avoid false positives (e.g., "class" vs "ass")
ABUSE_PATTERN_STRICT = re.compile(r"(?i)\b(" + "|".join(re.escape(word) for word in BANNED_WORDS) + r")\b")

# Relaxed pattern for hidden/embedded words (no word boundaries)
ABUSE_PATTERN_RELAXED = re.compile(r"(?i)(" + "|".join(re.escape(word) for word in BANNED_WORDS) + r")")

def _run_regex_sync(text):
    """Zenith Deep Scan Engine: Captures abuses inside full sentences."""
    if not text:
        return False, None

    # 1. Unicode Normalization (Catches stylized bypass fonts)
    normalized_text = unicodedata.normalize("NFKD", text).lower()
    
    # 2. Direct Sentence Scan (Captures: "sex is good" or "you bitch")
    # This pass uses word boundaries to catch distinct words clearly
    if ABUSE_PATTERN_STRICT.search(normalized_text):
        return True, "Abusive Language Detected"

    # 3. Embedded Word Scan (Captures: "dumbass" or "scumbag")
    # This checks if a banned word is part of a larger string (e.g. "motherfucker")
    if ABUSE_PATTERN_RELAXED.search(normalized_text):
        return True, "Abusive Language Detected"

    # 4. Hidden Word Scan (Captures: "s.e.x" or "f u c k")
    # We remove symbols/spaces to find distributed characters
    # Only alphanumeric characters remain
    noise_free = re.sub(r'[^a-z0-9]', '', normalized_text)
    if ABUSE_PATTERN_RELAXED.search(noise_free):
        return True, "Attempted Profanity Bypass"

    # 5. Link Protection
    if "makaut" not in normalized_text:
        for domain in SPAM_DOMAINS:
            if domain in normalized_text:
                return True, "Unauthorized Link"

    return False, None

async def is_inappropriate(text: str) -> (bool, str):
    """Asynchronous wrapper for the forensic scanner."""
    if not text:
        return False, None
    return await asyncio.to_thread(_run_regex_sync, text)