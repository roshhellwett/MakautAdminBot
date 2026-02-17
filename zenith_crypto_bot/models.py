from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

CryptoBase = declarative_base()

class CryptoUser(CryptoBase):
    __tablename__ = "crypto_users"
    user_id = Column(BigInteger, primary_key=True)
    alerts_enabled = Column(Boolean, default=False)
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Subscription(CryptoBase):
    __tablename__ = "crypto_subscriptions"
    user_id = Column(BigInteger, primary_key=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ActivationKey(CryptoBase):
    __tablename__ = "crypto_activation_keys"
    key_string = Column(String(50), primary_key=True)
    duration_days = Column(Integer, nullable=False)
    is_used = Column(Boolean, default=False)
    used_by = Column(BigInteger, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SavedAudit(CryptoBase):
    __tablename__ = "crypto_saved_audits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, index=True, nullable=False)
    contract = Column(String(150), nullable=False)
    saved_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # 🚀 FAANG FIX: Mathematically prevents duplicate records at the DB engine level
    __table_args__ = (UniqueConstraint('user_id', 'contract', name='uix_user_contract'),)