from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.db.session import async_session


@asynccontextmanager
async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
