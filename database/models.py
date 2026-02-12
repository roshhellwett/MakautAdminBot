from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source = Column(String, nullable=True)
    source_url = Column(String, nullable=False)
    pdf_url = Column(String, nullable=True)
    content_hash = Column(String, unique=True, index=True, nullable=False)
    published_date = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, nullable=True)

class SystemFlag(Base):
    __tablename__ = "system_flags"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(String(100), nullable=True)

# REMOVED: UserStrike (Moved to security_models.py for isolation)