from app.core.authentication import MyAuthBackEnd
from app.routers import auth as auth_router

from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware


app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=MyAuthBackEnd())

app.include_router(auth_router.router, prefix='/auth', tags=['Authentication'])
