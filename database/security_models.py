from sqlalchemy import Column, Integer, DateTime
from database.security_db import SecurityBase

class UserStrike(SecurityBase):
    """Isolated strike tracking for the security.db file."""
    __tablename__ = "user_strikes"
    user_id = Column(Integer, primary_key=True, index=True)
    strike_count = Column(Integer, default=0)
    last_violation = Column(DateTime, nullable=True)