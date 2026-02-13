from sqlalchemy import Column, Integer, BigInteger, DateTime
from database.db import Base  # Importing SHARED Base

class UserStrike(Base):
    """
    Security Table: Tracks user violations.
    Persists across re-deployments thanks to PostgreSQL.
    """
    __tablename__ = "user_strikes"
    
    # CRITICAL FIX: Changed Integer -> BigInteger
    # Telegram IDs (e.g., 7940390110) exceed the 32-bit Integer limit (2.1 billion)
    user_id = Column(BigInteger, primary_key=True, index=True)
    
    strike_count = Column(Integer, default=0)
    last_violation = Column(DateTime, nullable=True)
    #@academictelebotbyroshhellwett