import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_LEVEL = os.getenv('LOG_LEVEL')


# Настройки для отправки email-сообщения куратору
PORT_SMTP_SERVER = 587
SMTP_SERVER = 'smtp.yandex.ru'
EMAIL_BOT = os.getenv('EMAIL_BOT', 'FondProvidenieBot@yandex.ru')
EMAIL_CURATOR = os.getenv('EMAIL_CURATOR', 'k.danilow2009@yandex.ru') # ЗАМЕНИТЬ НА МЫЛО КУРАТОРА ФОНДА
EMAIL_BOT_PASSWORD = os.getenv('EMAIL_BOT_PASSWORD', 'jyvsejdjxyixsxkh')
TELEGRAM_CURATOR = os.getenv('TELEGRAM_CURATOR')
