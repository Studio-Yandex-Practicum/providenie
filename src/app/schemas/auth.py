from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Модель запроса на вход.

    Attributes:
        user_name (str): Имя пользователя.
        password (str): Пароль пользователя.

    """

    user_name: str
    password: str


class UserCreate(LoginRequest):
    """Модель для создания нового пользователя.

    Наследует:
        LoginRequest: Содержит имя пользователя и пароль.

    Attributes:
        first_name (str): Имя пользователя.
        tg_id (str): Идентификатор пользователя в Telegram.
        is_admin (bool): Флаг, является ли пользователь администратором.

    """

    first_name: str
    tg_id: str
    is_admin: bool = False
    password: Optional[str] = None
