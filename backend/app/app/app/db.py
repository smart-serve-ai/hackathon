from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

async_engine = create_async_engine(str(settings.db_dsn), echo=True)
AsyncDatabaseSession = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)
