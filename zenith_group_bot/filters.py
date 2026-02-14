import re
from zenith_group_bot.word_list import BANNED_WORDS

def contains_profanity_or_spam(text: str) -> bool:
    if not text: return False
    text = text.lower()
    for word in BANNED_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text):
            return True
    return False