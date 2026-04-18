from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import config

# Create async engine
engine = create_async_engine(
    config.DATABASE_URL.get_secret_value(),
    echo=False,  # True for initial testing
)

# Async session factory
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
