import contextlib

from app.core.db import get_async_session
from app.crud.user_tg import crud_user
from app.schemas.user_tg import UserCreate

from bot.core.settings import settings

get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def create_first_superuser():  # noqa: ANN201
    """Create first superuser."""
    if (settings.first_superuser_tg_id is not None
            and settings.first_superuser_first_name is not None
            and settings.first_superuser_user_name is not None
            and settings.first_superuser_password is not None):
        first_superuser = UserCreate(
            tg_id=settings.first_superuser_tg_id,
            first_name=settings.first_superuser_first_name,
            user_name=settings.first_superuser_user_name,
            is_admin=settings.first_superuser_is_admin,
            password=settings.first_superuser_password)

    try:
        async with get_async_session_context() as session:
            existing_user = await crud_user.get_one_by_attributes(
                {"tg_id": settings.first_superuser_tg_id}, session)
            if existing_user:
                raise Exception
            await crud_user.create(
                pydantic_scheme_user=first_superuser,
                session=session)
    except Exception:
        pass
