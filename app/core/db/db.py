from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core import settings

Base = declarative_base()

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,
)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
