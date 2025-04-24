import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncDatabaseSession

logger = logging.getLogger(__name__)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncDatabaseSession() as db:
        try:
            yield db
        finally:
            await db.close()
