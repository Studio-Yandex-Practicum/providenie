import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.auth import create_access_token
from src.app.core.authentication import MyUser
from src.app.core.db import get_async_session
from src.app.crud.user_tg import crud_user
from src.app.models.models import UserTG
from src.app.schemas.auth import UserCreate


router = APIRouter()


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),  # noqa: W0613
) -> MyUser:
    """Получение текущего пользователя.

    Args:
        request (Request): HTTP запрос.
        session (AsyncSession): Асинхронная сессия для взаимодействия с БД.

    Returns:
        MyUser: Пользователь, полученный из запроса.

    Raises:
        HTTPException: Если пользователь не аутентифицирован.

    """
    if not request.user:
        raise HTTPException(status_code=401, detail='UNAUTHORIZED')

    user = await session.execute(
        select(UserTG).where(UserTG.user_name == request.user.username),
    )
    if not user.scalar():
        raise HTTPException(status_code=404, detail='Пользователь не неайден.')

    return request.user


async def get_current_admin(
    user: MyUser = Depends(get_current_user),
) -> MyUser:
    """Проверка права администратора.

    Args:
        user (MyUser): Пользователь, полученный из запроса.

    Returns:
        MyUser: Пользователь с подтверждёнными правами администратора.

    Raises:
        HTTPException: Если пользователь не обладает правами администратора.

    """
    if not hasattr(user, 'is_admin') or not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='Доступ запрещён: требуются права администратора',
        )
    return user


@router.post('/login/')
async def login(
    response: Response,
    user_name: str,
    password: str,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Аутентификация пользователя и создание токена доступа.

    Args:
        response (Response): Объект ответа для установки cookie.
        user_name (str): Имя пользователя.
        password (str): Пароль пользователя.
        session (AsyncSession): Асинхронная сессия для взаимодействия с БД.

    Returns:
        dict: Сообщение о статусе аутентификации.

    Raises:
        HTTPException: Если данные пользователя неверны.

    """
    user = await crud_user.get_user_by_username(session, user_name)

    if not user:
        raise HTTPException(status_code=401, detail='Неверные учётные данные')

    if not bcrypt.checkpw(
        password.encode('utf-8'),
        user.hashed_password.encode('utf-8'),
    ):
        raise HTTPException(status_code=401, detail='Неверные учётные данные')

    token = create_access_token({'user_id': user.id})
    response.set_cookie(key='access_token', value=token, httponly=True)
    return {'message': 'Вход выполнен успешно'}


@router.post('/logout/')
async def logout(response: Response) -> dict:
    """Выход из системы.

    Args:
        response (Response): Объект ответа для удаления cookie.

    Returns:
        dict: Сообщение о статусе выхода.

    """
    response.delete_cookie('access_token')
    return {'message': 'Выход выполнен успешно'}


@router.get('/items/', dependencies=[Depends(get_current_admin)])
async def read_items(user: MyUser = Depends(get_current_user)) -> dict:
    """Получение информации о пользователе.

    Args:
        user (MyUser): Текущий аутентифицированный пользователь.

    Returns:
        dict: Информация о пользователе.

    """
    return {'user': user.display_name}


@router.post('/register/', response_model=dict)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Регистрирация нового пользователя.

    Args:
        user (UserCreate): Данные нового пользователя.
        session (AsyncSession): Асинхронная сессия для взаимодействия с БД.

    Returns:
        dict: Сообщение об успешной регистрации.

    Raises:
        HTTPException: Если пользователь с таким именем уже существует.

    """
    existing_user = await crud_user.get_user_by_username(
        session,
        user.user_name,
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='User with this username already exists',
        )

    new_user = await crud_user.create(user, session)
    return {
        'message': 'User created successfully',
        'user_name': new_user.user_name,
    }
