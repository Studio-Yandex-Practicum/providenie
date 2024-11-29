from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Модель запроса на вход.

    Attributes:
        user_name (str): Имя пользователя.
        password (str): Пароль пользователя.

    """

    user_name: str
    password: str


class UserCreate(BaseModel):
    """Модель для создания нового пользователя."""

    user_name: str
    password: str
    first_name: str
    tg_id: str
    is_admin: bool = False
