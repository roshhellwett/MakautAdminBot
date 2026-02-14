import re
from zenith_group_bot.word_list import BANNED_WORDS

# Compile regex at startup (O(1) time complexity) instead of per message
_PATTERN_STRING = r'\b(' + '|'.join(map(re.escape, BANNED_WORDS)) + r')\b'
BANNED_REGEX = re.compile(_PATTERN_STRING, re.IGNORECASE)

async def is_inappropriate(text: str) -> tuple[bool, str]:
    if not text: 
        return False, ""
        
    if BANNED_REGEX.search(text):
        return True, "Banned vocabulary detected."
            
    return False, ""