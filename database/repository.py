import logging
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from database.db import AsyncSessionLocal
from database.models import Notification
from database.security_db import SecuritySessionLocal
from database.security_models import UserStrike

logger = logging.getLogger("DB_REPO")

class NotificationRepo:
    """Academic Data Access Layer (DAL)"""
    
    @staticmethod
    async def add_notification(data: dict) -> bool:
        """Idempotent insert: Returns True if new, False if exists."""
        async with AsyncSessionLocal() as db:
            try:
                # Check hash existence first (Fast Index Scan)
                stmt = select(Notification.id).where(Notification.content_hash == data['content_hash'])
                exists = (await db.execute(stmt)).scalar()
                
                if not exists:
                    db.add(Notification(**data))
                    await db.commit()
                    return True
                return False
            except IntegrityError:
                await db.rollback()
                return False
            except Exception as e:
                logger.error(f"Insert Failed: {e}")
                return False

    @staticmethod
    async def get_latest(limit: int = 10):
        """Fetch recent notices ordered by publication date."""
        async with AsyncSessionLocal() as db:
            stmt = select(Notification).order_by(Notification.published_date.desc()).limit(limit)
            return (await db.execute(stmt)).scalars().all()

    @staticmethod
    async def search_query(keyword: str, limit: int = 10):
        """Case-insensitive title search."""
        async with AsyncSessionLocal() as db:
            stmt = select(Notification).filter(
                Notification.title.ilike(f"%{keyword}%")
            ).order_by(Notification.published_date.desc()).limit(limit)
            return (await db.execute(stmt)).scalars().all()

    @staticmethod
    async def get_stats():
        """Returns total count of notices."""
        async with AsyncSessionLocal() as db:
            return (await db.execute(select(func.count(Notification.id)))).scalar()

class SecurityRepo:
    """Security/Moderation Data Access Layer (DAL)"""
    
    @staticmethod
    async def get_active_strikes():
        """Count users with active strikes."""
        async with SecuritySessionLocal() as db:
            return (await db.execute(select(func.count(UserStrike.user_id)))).scalar()