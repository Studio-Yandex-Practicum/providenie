import asyncio
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.authentication import AuthenticationMiddleware

from app.admin_endpoints.routers import main_router
from app.config import BASE_DIR  # noqa: I001
from app.core.authentication import MyAuthBackEnd
from app.routers import auth as auth_router

from bot.core import logger  # noqa
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


@app.get('/')
def read_root() -> Dict[str, str]:
    """Return a welcome message in JSON format."""
    return {'message': 'Hello, the API is working!'}


@app.exception_handler(404)
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
        {'request': request},
        status_code=404,
    )


@app.exception_handler(401)
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
        '401.html',
        {'request': request},
        status_code=401,
    )


async def run_bot() -> None:
    """Launch the Telegram bot."""
    await bot_application.initialize()
    await bot_application.start()
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
