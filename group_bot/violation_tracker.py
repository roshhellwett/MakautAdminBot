import logging
from datetime import datetime
from sqlalchemy import select
from database.security_db import SecuritySessionLocal
from database.security_models import UserStrike

logger = logging.getLogger("VIOLATION_TRACKER")

STRIKE_LIMIT = 3

async def add_strike(user_id: int) -> bool:
    """Increments strikes using the isolated Security Database."""
    async with SecuritySessionLocal() as db:
        try:
            stmt = select(UserStrike).where(UserStrike.user_id == user_id)
            result = await db.execute(stmt)
            record = result.scalar_one_or_none()

            if not record:
                record = UserStrike(
                    user_id=user_id, 
                    strike_count=1, 
                    last_violation=datetime.utcnow()
                )
                db.add(record)
                await db.commit()
                return False
            
            record.strike_count += 1
            record.last_violation = datetime.utcnow()
            limit_hit = record.strike_count >= STRIKE_LIMIT
            
            if limit_hit:
                record.strike_count = 0
                logger.warning(f"🚫 User {user_id} hit strike limit in Security DB.")

            await db.commit()
            return limit_hit
        except Exception as e:
            logger.error(f"Security DB strike update failed: {e}")
            return False