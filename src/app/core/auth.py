from datetime import datetime, timedelta
from typing import Optional

import jwt
from jwt import PyJWTError

from src.bot.core.settings import settings


# from src.bot.core import settings


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Создаёт JWT-токен с заданными данными и временем истечения.

    Returns:
        str: Сгенерированный JWT-токен.

    """
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def verify_token(token: str) -> Optional[dict]:
    """Проверка валидности JWT-токена.

    Args:
        token (str): JWT-токен для проверки.

    Returns:
        Optional[dict]: Раскодированные данные токена, если он валиден.
        None: Если токен недействителен или истёк.

    """
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except PyJWTError:
        return None
