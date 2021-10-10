from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DB_ECHO_LOG,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
