import asyncio

import uvicorn
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.authentication import AuthenticationMiddleware

from app.admin_endpoints.routers import main_router
from app.config import BASE_DIR  # noqa: I001
from app.core.auth import get_current_admin
from app.core.authentication import MyAuthBackEnd
from app.routers import auth as auth_router

from bot.core import logger  # noqa
from bot.ratelimiter import ptb_post_init
from bot.services import bot_application

app = FastAPI()
app.include_router(main_router)
app.include_router(auth_router.router, prefix='/auth', tags=['Authentication'])
templates = Jinja2Templates(directory=BASE_DIR / 'app/templates')

app.mount(
    '/static',
    StaticFiles(directory='app/static'),
    name='static',
)
app.add_middleware(AuthenticationMiddleware, backend=MyAuthBackEnd())

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', dependencies=[Depends(get_current_admin)])
def read_root(
    request: Request,
) -> HTMLResponse:
    """Redirect to dashboard."""
    return RedirectResponse(
        url='/admin/',
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found_error(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    """Обработка ошибки 404.

    Args:
        request (Request): Объект запроса.
        exc (StarletteHTTPException): Исключение, вызвавшее ошибку 404.

    Returns:
        Response: HTML-ответ с шаблоном 404 и статусом 404.

    """
    return templates.TemplateResponse(
        '404.html',
        {
            'request': request,
            'detail': str(exc.detail) if exc.detail else 'Неизвестная ошибка.',
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_error(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    """Обработка ошибки 401.

    Args:
        request (Request): Объект запроса.
        exc (StarletteHTTPException): Исключение, вызвавшее ошибку 401.

    Returns:
        Response: HTML-ответ с шаблоном 401 и статусом 401.

    """
    return templates.TemplateResponse(
        'login.html',
        {
            'request': request,
            'message': str(exc.detail)
            if exc.detail
            else 'Неизвестная ошибка.',
        },
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


@app.exception_handler(status.HTTP_400_BAD_REQUEST)
async def bad_request_error(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    """Обработка ошибки 400.

    Args:
        request (Request): Объект запроса.
        exc (StarletteHTTPException): Исключение, вызвавшее ошибку 400.

    Returns:
        Response: HTML-ответ с шаблоном 400 и статусом 400.

    """
    return templates.TemplateResponse(
        '400.html',
        {
            'request': request,
            'detail': str(exc.detail) if exc.detail else 'Неизвестная ошибка.',
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(status.HTTP_403_FORBIDDEN)
async def forbidden_error(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    """Обработка ошибки 403.

    Args:
        request (Request): Объект запроса.
        exc (StarletteHTTPException): Исключение, вызвавшее ошибку 403.

    Returns:
        Response: HTML-ответ с шаблоном 403 и статусом 403.

    """
    return templates.TemplateResponse(
        '403.html',
        {
            'request': request,
            'detail': str(exc.detail) if exc.detail else 'Неизвестная ошибка.',
        },
        status_code=status.HTTP_403_FORBIDDEN,
    )


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def internal_server_error(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    """Обработка ошибки 500.

    Args:
        request (Request): Объект запроса.
        exc (StarletteException): Исключение, вызвавшее ошибку 500.

    Returns:
        Response: HTML-ответ с шаблоном 500 и статусом 500.

    """
    return templates.TemplateResponse(
        '500.html',
        {
            'request': request,
            'detail': str(exc.detail) if exc.detail else 'Неизвестная ошибка.',
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(Exception)
async def all_other_errors(
    request: Request,
    exc: Exception,
) -> Response:
    """Обработка остальных ошибок.

    Args:
        request (Request): Объект запроса.
        exc (Exception): Исключение, вызвавшее ошибку.

    Returns:
        Response: HTML-ответ с шаблоном 500 и статусом 500.

    """
    return templates.TemplateResponse(
        '500.html',
        {
            'request': request,
            'detail': str(exc) if exc else 'Неизвестная ошибка.',
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def run_bot() -> None:
    """Launch the Telegram bot."""
    await bot_application.initialize()
    await bot_application.start()
    await ptb_post_init(bot_application)
    await bot_application.updater.start_polling()


async def run_fastapi() -> None:
    """Launch the FastAPI application."""
    config = uvicorn.Config(app, host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    """Run both the Telegram bot and FastAPI concurrently."""
    await asyncio.gather(run_bot(), run_fastapi())


if __name__ == '__main__':
    asyncio.run(main())
