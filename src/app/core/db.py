from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from bot.core.settings import settings


class PreBase:
    """Базовый класс для моделей, содержащий общие поля.

    Этот класс используется для автоматического создания таблиц в базе данных.
    Классы, наследующие от PreBase, получат следующие поля:
    - id: уникальный идентификатор, который является первичным ключом.
    - created_at: метка времени для отслеживания времени создания записи.
    - updated_at: метка времени для отслеживания времени последнего обновления.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    )


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url, future=True, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор для создания и получения асинхронной сессии SQLAlchemy.

    Этот метод позволяет использовать сессию для взаимодействия с базой данных.
    :yield: объект сессии для работы с базой данных.
    """
    async with AsyncSessionLocal() as session:
        yield session
