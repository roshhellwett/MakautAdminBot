import time
from collections import deque

# Zenith Production Tuning
# Specifically balanced for database protection vs user search speed
MAX_MESSAGES = 4          # Max 4 searches allowed per time window
TIME_WINDOW = 12          # 12-second window to prevent database query spikes
DUPLICATE_LIMIT = 1       # Blocks the exact same query twice in a row

# User activity storage: {user_id: [timestamps]}
user_history = {}
# Duplicate message storage: {user_id: {"text": str, "count": int}}
user_duplicates = {}

def is_flooding(user_id: int, message_text: str) -> (bool, str):
    """
    Forensic analyzer for search and group messaging.
    Returns (True, reason) if user is spamming, otherwise (False, None).
    """
    now = time.time()
    
    # --- 1. Frequency Analysis (Token Bucket) ---
    if user_id not in user_history:
        user_history[user_id] = deque()
    
    timestamps = user_history[user_id]
    timestamps.append(now)
    
    # Clear history outside the sliding time window
    while timestamps and timestamps[0] < now - TIME_WINDOW:
        timestamps.popleft()
    
    if len(timestamps) > MAX_MESSAGES:
        return True, "Too many requests. Please wait a few seconds."

    # --- 2. Content Repetition Analysis ---
    text_clean = message_text.lower().strip()
    if user_id not in user_duplicates:
        user_duplicates[user_id] = {"text": "", "count": 0}
    
    # Check if this query is identical to the last one
    if user_duplicates[user_id]["text"] == text_clean:
        user_duplicates[user_id]["count"] += 1
    else:
        user_duplicates[user_id]["text"] = text_clean
        user_duplicates[user_id]["count"] = 1
     
    if user_duplicates[user_id]["count"] > DUPLICATE_LIMIT:
        return True, "Identical query detected. Use different keywords."

    return False, None
    #@academictelebotbyroshhellwett