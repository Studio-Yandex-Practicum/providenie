import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

is_run_in_docker = bool(int(os.environ.get('RUN_IN_DOCKER', '0')))


class Settings(BaseSettings):
    """Model application settings."""

    telegram_token: str

    log_level: str = 'INFO'
    log_filename: str = 'bot.log'
    log_format: str = '%(asctime)s, %(levelname)s, %(name)s, %(message)s'

    debug: bool = False

    smtp_server_port: int = 465
    smtp_server_address: str = 'smtp.yandex.ru'
    smtp_server_bot_email: str = ''
    smtp_server_bot_password: str = ''

    email_curator: str = ''
    database_url: str

    SECRET_KEY: str = 'my_secret_key'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_server: str
    postgres_port: str

    token_secret_key: str = 'my_secret_key'
    token_algorithm: str = 'HS256'
    token_expire_minutes: int = 30

    first_superuser_tg_id: str
    first_superuser_first_name: str
    first_superuser_user_name:str
    first_superuser_password:str
    first_superuser_is_admin: bool

    class Config:  # noqa: D106
        env_file = None if is_run_in_docker else BASE_DIR / 'infra/.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

    @property
    def database_url(self) -> str:
        """Возвращает строку подключения к БД."""
        host = self.postgres_server if is_run_in_docker else 'localhost'
        return (
            f'postgresql+asyncpg://{self.postgres_user}:'
            f'{self.postgres_password}@{host}:{self.postgres_port}'
            f'/{self.postgres_db}'
        )


settings = Settings()
