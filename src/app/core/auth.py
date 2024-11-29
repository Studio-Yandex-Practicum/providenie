from fastapi import Depends, HTTPException, Request

from app.core.constants import KEY_IS_ADMIN
from app.models.models import UserTG


async def get_current_user(
    request: Request,
) -> UserTG:
    """Получение текущего пользователя."""
    if not request.user:
        raise HTTPException(status_code=401, detail='UNAUTHORIZED')
    if getattr(request.user, 'is_blocked', False):
        raise HTTPException(status_code=403, detail='User is blocked.')

    return request.user


async def get_current_admin(
    user: UserTG = Depends(get_current_user),
) -> UserTG:
    """Проверка права администратора."""
    if not hasattr(user, KEY_IS_ADMIN) or not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='Доступ запрещён: требуются права администратора',
        )
    return user
