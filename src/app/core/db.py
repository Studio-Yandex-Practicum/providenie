from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from src.bot.core.settings import settings


class PreBase:
    """Initial db class with general columns."""

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.lower()

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    )


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url, future=True)

AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession,
)


async def get_async_session():  # noqa: ANN201
    """Asynchronous session generator."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
