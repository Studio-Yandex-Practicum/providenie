import bcrypt
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.config import BASE_DIR
from src.app.core.auth import create_access_token
from src.app.core.authentication import MyUser
from src.app.core.db import get_async_session
from src.app.crud.user_tg import crud_user
from src.app.models.models import UserTG
from src.app.schemas.auth import UserCreate

router = APIRouter()

templates = Jinja2Templates(directory=BASE_DIR / 'app/templates')


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


@router.get('/login/', response_class=HTMLResponse)
async def show_login_page(request: Request, message: str = None) -> Response:
    """Показывает страницу входа."""
    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'message': message},
    )


@router.post('/login/')
async def login(
    response: Response,
    request: Request,
    user_name: str = Form(...),
    password: str = Form(...),
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
        return templates.TemplateResponse(
            'login.html',
            {'request': request, 'message': 'Неверные данные для входа'},
            status_code=401,
        )

    if not bcrypt.checkpw(
        password.encode('utf-8'),
        user.hashed_password.encode('utf-8'),
    ):
        return templates.TemplateResponse(
            'login.html',
            {'request': request, 'message': 'Неверные данные для входа'},
            status_code=401,
        )

    token = create_access_token({'user_id': user.id})
    response = RedirectResponse(
        url='/auth/dashboard/',
        status_code=303,
    )
    response.set_cookie(
        key='access_token',
        value=token,
        samesite='Lax',
        httponly=True,
    )
    return response


@router.post('/logout/')
async def logout(response: Response) -> dict:
    """Выход из системы.

    Args:
        response (Response): Объект ответа для удаления cookie.

    Returns:
        dict: Сообщение о статусе выхода.

    """
    response = RedirectResponse(url='/auth/login/', status_code=303)
    response.delete_cookie('access_token')
    return response


@router.get('/items/', dependencies=[Depends(get_current_admin)])
async def read_items(user: MyUser = Depends(get_current_user)) -> dict:
    """Получение информации о пользователе.

    Args:
        user (MyUser): Текущий аутентифицированный пользователь.

    Returns:
        dict: Информация о пользователе.

    """
    return {'user': user.display_name}


@router.get('/register/', response_class=HTMLResponse)
async def show_register_page(request: Request) -> Response:
    """Показывает страницу регистрации."""
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register/', response_model=dict)
async def register_user(
    user_name: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    tg_id: str = Form(...),
    is_admin: bool = Form(False),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Регистрирация нового пользователя.

    Args:
        user_name: Логин пользователя.
        password: Пароль.
        first_name: Имя пользователя.
        tg_id: Телеграмм id.
        is_admin: False
        session (AsyncSession): Асинхронная сессия для взаимодействия с БД.

    Returns:
        dict: Сообщение об успешной регистрации.

    Raises:
        HTTPException: Если пользователь с таким именем уже существует.

    """
    user = UserCreate(
        first_name=first_name,
        user_name=user_name,
        password=password,
        tg_id=tg_id,
        is_admin=is_admin,
    )
    existing_user = await crud_user.get_user_by_username(
        session,
        user.user_name,
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже существует',
        )

    await crud_user.create(pydantic_scheme_user=user, session=session)
    return RedirectResponse(url='/auth/login/', status_code=303)


@router.get('/dashboard/', response_class=HTMLResponse)
async def dashboard(request: Request) -> Response:
    """Пустая страница после успешного входа."""
    return templates.TemplateResponse(
        'dashboard.html',
        {'request': request},
    )
