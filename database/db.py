import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from core.config import DATABASE_URL

logger = logging.getLogger("DATABASE")

# SMART PROTOCOL CHECK: Prevents malformed URLs and unpacking errors
if "aiosqlite" in DATABASE_URL:
    ASYNC_DB_URL = DATABASE_URL
else:
    if DATABASE_URL.startswith("sqlite:///"):
        ASYNC_DB_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
    elif DATABASE_URL.startswith("sqlite://"):
        ASYNC_DB_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    else:
        ASYNC_DB_URL = DATABASE_URL

# Standard SQLAlchemy 2.0 Async engine with multi-thread safety for SQLite
engine = create_async_engine(
    ASYNC_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()
logger.info(f"DATABASE ENGINE READY (ASYNC MODE: {ASYNC_DB_URL.split('+')[0]})")