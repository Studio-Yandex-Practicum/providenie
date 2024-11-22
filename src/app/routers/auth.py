from fastapi import APIRouter, Depends, HTTPException, Response
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token, get_current_user
from app.core.db import get_async_session
from app.models.models import UserTG

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/login')
async def login(
    tg_id: int,
    password: str,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Авторизация пользователя."""
    user = await session.execute(
        select(UserTG).filter(UserTG.tg_id == tg_id),
    )
    user = user.scalar_one_or_none()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    token = create_access_token({'sub': str(user.id)})
    response.set_cookie(key='access_token', value=token, httponly=True)
    return {'access_token': token}


@router.get('/me')
async def get_me(user: UserTG = Depends(get_current_user)) -> dict:
    """Получение текущего пользователя."""
    return {'id': user.id, 'user_name': user.user_name}
