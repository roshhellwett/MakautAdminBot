import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

logger = logging.getLogger("SECURITY_DB")

# Isolated database for moderation data
SECURITY_DATABASE_URL = "sqlite+aiosqlite:///security.db"

security_engine = create_async_engine(
    SECURITY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
    echo=False
)

SecuritySessionLocal = sessionmaker(
    security_engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

SecurityBase = declarative_base()
logger.info("SECURITY DATABASE ENGINE READY (Isolated Storage: security.db)")
#@academictelebotbyroshhellwett