from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import BASE_DIR
from app.core.auth import get_current_admin, get_current_user
from app.core.constants import KEY_ACCESS_TOKEN
from app.core.db import get_async_session
from app.core.jwt import create_access_token, password_verify
from app.crud.user_tg import crud_user
from app.models.models import UserTG
from app.schemas.auth import UserCreate

router = APIRouter()

templates = Jinja2Templates(directory=BASE_DIR / 'app/templates')


@router.get('/login/', response_class=HTMLResponse, name='auth_login')
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
) -> Response:
    """Аутентификация пользователя и установка токена в cookie.

    Args:
        response (Response): Объект ответа для установки cookie.
        request (Request): Объект запроса.
        user_name (str): Имя пользователя.
        password (str): Пароль пользователя.
        session (AsyncSession): Асинхронная сессия для взаимодействия с бд.

    Returns:
        Response: Перенаправление на страницу панели управления
        или форма входа с ошибкой.

    """
    user = await crud_user.get_one_by_attributes(
        filters={'user_name': user_name},
        session=session,
    )
    if not user or not password_verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверный логин/пароль')

    token = create_access_token(str(user.id))
    response = RedirectResponse(
        url='/admin/',
        status_code=303,
    )
    response.set_cookie(
        key=KEY_ACCESS_TOKEN,
        value=token,
        samesite='Lax',
        httponly=True,
    )
    return response


@router.get('/logout/')
async def logout(response: Response) -> Response:
    """Выход из системы и удаление токена из cookie.

    Args:
        response (Response): Объект ответа.

    Returns:
        Response: Перенаправление на страницу входа.

    """
    response = RedirectResponse(url='/auth/login/', status_code=303)
    response.delete_cookie(KEY_ACCESS_TOKEN)
    return response


@router.get('/items/', dependencies=[Depends(get_current_admin)])
async def read_items(user: UserTG = Depends(get_current_user)) -> dict:
    """Получение информации о пользователе.

    Args:
        user (MyUser): Текущий аутентифицированный пользователь.

    Returns:
        dict: Информация о пользователе.

    """
    return {'user': user.display_name}


@router.get('/register/', response_class=HTMLResponse, name='auth_register')
async def show_register_page(request: Request) -> HTMLResponse:
    """Показывает страницу регистрации.

    Args:
        request (Request): Объект запроса.

    Returns:
        HTMLResponse: Шаблон страницы регистрации.

    """
    return templates.TemplateResponse('register.html', {'request': request})


@router.post(
    '/register/',
    response_model=dict,
    dependencies=[Depends(get_current_admin)],
)
async def register_user(
    user_name: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    tg_id: str = Form(...),
    is_admin: bool = Form(False),
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """Регистрация нового пользователя.

    Args:
        user_name (str): Логин пользователя.
        password (str): Пароль пользователя.
        first_name (str): Имя пользователя.
        tg_id (str): Telegram ID.
        is_admin (bool): Признак администратора.
        session (AsyncSession): Асинхронная сессия для взаимодействия с бд.

    Returns:
        Response: Перенаправление на страницу входа.

    Raises:
        HTTPException: Если пользователь с таким логином уже существует.

    """
    user = UserCreate(
        first_name=first_name,
        user_name=user_name,
        password=password,
        tg_id=tg_id,
        is_admin=is_admin,
    )
    existing_user = await crud_user.get_one_by_attributes(
        filters={'user_name': user.user_name},
        session=session,
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже существует',
        )

    await crud_user.create(pydantic_scheme_user=user, session=session)
    return RedirectResponse(url='/login/', status_code=303)


@router.get('/dashboard/', response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    """Показывает страницу панели управления.

    Args:
        request (Request): Объект запроса.

    Returns:
        HTMLResponse: Шаблон страницы панели управления.

    """
    return templates.TemplateResponse(
        'dashboard.html',
        {'request': request},
    )
