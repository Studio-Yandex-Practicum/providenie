from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from src.bot.core.settings import settings


class PreBase:
    """Base class for all tables."""

    @declared_attr
    def __tablename__(cls):  # noqa: ANN204, N805
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Asynchronous session generator."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
