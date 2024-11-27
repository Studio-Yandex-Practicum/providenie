from src.app.config import BASE_DIR
from src.app.core.authentication import MyAuthBackEnd
from src.app.routers import auth as auth_router

from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=MyAuthBackEnd())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router.router, prefix='/auth', tags=['Authentication'])

templates = Jinja2Templates(directory=BASE_DIR / 'app/templates')


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
