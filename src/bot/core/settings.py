from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


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

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_server: str
    postgres_port: str
    database_url: str

    class Config:  # noqa: D106
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()
