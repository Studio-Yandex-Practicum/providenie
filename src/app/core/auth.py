from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.models import UserTG

from bot.core.settings import settings


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """Создаёт JWT токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


async def get_current_user(
    token: str,
    session: AsyncSession = Depends(get_async_session),
) -> UserTG:
    """Получает текущего пользователя на основе JWT токена."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: int = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail='Ошибка токена')
        user = await session.get(UserTG, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail='Пользователь не найден или неактивен',
            )
        return user
    except PyJWTError as exc:
        raise HTTPException(
            status_code=401,
            detail='Не удалось проверить токен',
        ) from exc
