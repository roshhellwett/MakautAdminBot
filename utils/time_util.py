from datetime import datetime, timezone
import zoneinfo


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_now_ist() -> datetime:
    ist_zone = zoneinfo.ZoneInfo("Asia/Kolkata")
    return datetime.now(ist_zone)