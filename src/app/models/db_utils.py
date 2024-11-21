from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta

from app.models.models import UserTG


async def fetch_one(session: AsyncSession, query: select) -> UserTG | None:
    """Выполняет запрос и возвращает одну запись из базы данных.

    :param session: Асинхронная сессия для работы с базой данных.
    :param query: Запрос SQLAlchemy, который нужно выполнить.

    :return: Возвращает один результат или None, если запись не найдена.
    """
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def save_and_commit(
    session: AsyncSession,
    instance: DeclarativeMeta,
) -> None:
    """Сохраняет объект в базе данных и выполняет коммит.

    :param session: Асинхронная сессия для работы с базой данных.
    :param instance: Экземпляр модели, который необходимо сохранить в базе.

    :return: None
    """
    session.add(instance)
    await session.commit()


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> UserTG:
    """Получает пользователя по его Telegram ID.

    :param session: Асинхронная сессия для работы с базой данных.
    :param tg_id: ID пользователя в Telegram.

    :return: Возвращает объект User или None, если не найден.
    """
    query = select(UserTG).where(UserTG.tg_id == tg_id)
    return await fetch_one(session, query)


async def create_or_update_user(
    session: AsyncSession,
    tg_user: UserTG,
) -> UserTG:
    """Создает нового пользователя или обновляет существующего.

    :param session: Асинхронная сессия для работы с базой данных.
    :param tg_user: Объект пользователя из Telegram,
    который содержит данные для создания или обновления.

    :return: Возвращает обновленный или созданный объект User.
    """
    user = await get_user_by_tg_id(session, tg_user.id)
    if user:
        user.first_name = tg_user.first_name
        user.last_name = tg_user.last_name
        user.user_name = tg_user.username
        user.is_active = True
    else:
        user = UserTG(
            tg_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            user_name=tg_user.username,
            is_active=True,
        )
    await save_and_commit(session, user)
    return user
