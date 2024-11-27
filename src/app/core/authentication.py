from fastapi.requests import HTTPConnection
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    SimpleUser,
)

from src.app.core.auth import verify_token
from src.app.core.db import get_async_session
from src.app.crud.user_tg import crud_user


class MyUser(SimpleUser):  # noqa: W0223
    """Пользовательский класс пользователя с расширенными атрибутами.

    Args:
        user_name (str): Имя пользователя.
        user_id (int): Уникальный идентификатор пользователя.
        is_admin (bool): Флаг, указывающий, является ли пользователь is_admin.

    """

    def __init__(  # noqa
        self,
        user_name: str,
        user_id: int,
        is_admin: bool,
    ) -> None:
        super().__init__(user_name)
        self.user_id = user_id
        self._is_admin = is_admin

    @property
    def is_admin(self) -> bool:
        """Возвращает статус администратора."""
        return self._is_admin


class MyAuthBackEnd(AuthenticationBackend):
    """Пользовательский класс для аутентификации пользователей через токен."""

    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> tuple[AuthCredentials, MyUser] | None:
        """Аутентификация пользователя по токену из cookies.

        Args:
            conn (HTTPConnection): Подключение HTTP, содержащее cookies.

        Returns:
            tuple[AuthCredentials, MyUser] | None:
                - Кортеж, содержащий AuthCredentials и MyUser,
                если токен валиден.
                - None, если токен отсутствует, недействителен
                или пользователь неактивен.

        """
        token = conn.cookies.get('access_token')
        if not token:
            return None

        payload = verify_token(token)
        if not payload:
            return None

        user_id = payload.get('user_id')
        async for session in get_async_session():
            user = await crud_user.get(session, user_id)
            if not user or not user.is_active:
                return None

        return AuthCredentials(['authenticated']), MyUser(
            user_name=user.user_name,
            user_id=user.id,
            is_admin=user.is_admin,
        )
