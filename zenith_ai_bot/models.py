from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Text, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

AIBase = declarative_base()


class AIConversation(AIBase):
    __tablename__ = "zenith_ai_conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True, nullable=False)
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AIUsageLog(AIBase):
    __tablename__ = "zenith_ai_usage"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True, nullable=False)
    usage_date = Column(Date, nullable=False)
    query_count = Column(Integer, default=0)
    summarize_count = Column(Integer, default=0)
    persona = Column(String(20), default="default")
