from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def get_now_ist():
    return datetime.now(IST)