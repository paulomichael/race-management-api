from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from core.configs import settings
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(settings.DB_URL, echo=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
