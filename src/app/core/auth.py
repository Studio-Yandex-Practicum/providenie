from fastapi import Depends, HTTPException, Request

from app.core.constants import KEY_IS_ADMIN
from app.models.models import UserTG


async def get_current_user(  # noqa: ANN201
    request: Request,
):
    """Получение текущего пользователя."""
    user = request.user
    if not isinstance(user, UserTG) and getattr(
        user, 'is_authenticated', False) is False:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')

    if getattr(user, 'is_block', False) is True:
        raise HTTPException(
            status_code=403,
            detail='Пользователь заблокирован')
    return user


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
