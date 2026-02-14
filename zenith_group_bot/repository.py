from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from datetime import datetime
from zenith_group_bot.models import Base, GroupStrike
from core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_group_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class GroupRepo:
    @staticmethod
    async def process_violation(user_id: int, chat_id: int):
        """Automatically partitions strikes by chat_id."""
        async with AsyncSessionLocal() as session:
            stmt = select(GroupStrike).where(
                GroupStrike.user_id == user_id, 
                GroupStrike.chat_id == chat_id
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            
            if not record:
                record = GroupStrike(user_id=user_id, chat_id=chat_id, strike_count=1, last_violation=datetime.utcnow())
                session.add(record)
            else:
                record.strike_count += 1
                record.last_violation = datetime.utcnow()
            
            await session.commit()
            return record.strike_count