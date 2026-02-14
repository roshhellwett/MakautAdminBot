import time
from collections import deque
from cachetools import TTLCache

# Standard user spam tracking
user_message_history = TTLCache(maxsize=10000, ttl=5.0)

# Scenario 7: Tracks albums. If 10 photos are sent at once, they share a media_group_id.
seen_albums = TTLCache(maxsize=5000, ttl=10.0)

def is_flooding(user_id: int, media_group_id: str = None) -> tuple[bool, str]:
    now = time.time()
    
    # Bypass spam counter if this message is part of an album we've already registered
    if media_group_id:
        if media_group_id in seen_albums:
            return False, ""
        seen_albums[media_group_id] = True
    
    if user_id not in user_message_history:
        user_message_history[user_id] = deque(maxlen=5)
        
    history = user_message_history[user_id]
    history.append(now)
    
    # Trigger if 5 unique messages arrive in under 3 seconds
    if len(history) == 5 and (history[-1] - history[0] < 3.0):
        return True, "Message Flooding (Spamming)"
        
    return False, ""