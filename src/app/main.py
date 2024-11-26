from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from src.app.core.authentication import MyAuthBackEnd
from src.app.routers import auth as auth_router

app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=MyAuthBackEnd())

app.include_router(auth_router.router, prefix='/auth', tags=['Authentication'])
