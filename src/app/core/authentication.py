from fastapi.requests import HTTPConnection
from starlette.authentication import AuthCredentials, AuthenticationBackend

from app.core.constants import (
    KEY_ACCESS_TOKEN,
    KEY_STATUS,
    KEY_USER_ID,
)
from app.core.db import get_async_session
from app.core.jwt import jwt_decode
from app.crud.user_tg import crud_user
from app.models.models import UserTG


class MyAuthBackEnd(AuthenticationBackend):
    """Пользовательский класс для аутентификации через токен."""

    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> tuple[AuthCredentials, UserTG] | None:
        """Аутентификация пользователя по токену из cookies."""
        token = conn.cookies.get(KEY_ACCESS_TOKEN)
        if not token:
            return None

        decoded_token = jwt_decode(token)
        if decoded_token.get(KEY_STATUS) != 'ok':
            return None

        user_id = int(decoded_token[KEY_USER_ID])

        async for session in get_async_session():
            user = await crud_user.get_obj_by_id(user_id, session)
            if not user or not user.is_active:
                return None

        return AuthCredentials(['authenticated']), user
