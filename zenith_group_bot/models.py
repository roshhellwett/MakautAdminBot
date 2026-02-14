from sqlalchemy import Column, Integer, BigInteger, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class GroupStrike(Base):
    """Multi-Group isolated strike tracking."""
    __tablename__ = "zenith_group_strikes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    chat_id = Column(BigInteger, index=True) # Isolates strikes per group
    strike_count = Column(Integer, default=0)
    last_violation = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint('user_id', 'chat_id', name='_user_chat_uc'),)