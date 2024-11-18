from pydantic import BaseSettings, Field


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

    postgres_user: str = Field(..., env='POSTGRES_USER')
    postgres_password: str = Field(..., env='POSTGRES_PASSWORD')
    postgres_db: str = Field(..., env='POSTGRES_DB')
    postgres_server: str = Field(default='localhost', env='POSTGRES_SERVER')
    postgres_port: int = Field(default=5432, env='POSTGRES_PORT')
    database_url: str = Field(..., env='DATABASE_URL')

    class Config:  # noqa: D106
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
