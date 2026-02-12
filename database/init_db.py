import logging
from database.db import Base, engine
from database.security_db import SecurityBase, security_engine
from database import models, security_models 

logger = logging.getLogger("DATABASE_INIT")

async def init_db():
    """Initializes all isolated database systems."""
    logger.info("Verifying all database systems...")
    try:
        # Initialize Academic DB (makaut.db)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Initialize Security DB (security.db)
        async with security_engine.begin() as s_conn:
            await s_conn.run_sync(SecurityBase.metadata.create_all)
            
        logger.info("✅ ALL DATABASES (ACADEMIC + SECURITY) VERIFIED")
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        raise e