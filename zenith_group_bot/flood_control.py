import time
from collections import defaultdict, deque

# Tracks message timestamps per user per group independently
user_message_history = defaultdict(lambda: deque(maxlen=5))

def is_flooding(user_id: int, chat_id: int) -> bool:
    key = f"{chat_id}_{user_id}"
    now = time.time()
    history = user_message_history[key]
    history.append(now)
    
    # Trigger if 5 messages are sent in under 3 seconds
    if len(history) == 5 and (history[-1] - history[0] < 3.0):
        return True
    return False