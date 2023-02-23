import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


# Настройки для отправки email-сообщения куратору
PORT_SMTP_SERVER = 587
SMTP_SERVER = 'smtp.yandex.ru'
EMAIL_BOT = os.getenv('EMAIL_BOT')
EMAIL_CURATOR = os.getenv('EMAIL_CURATOR')
EMAIL_BOT_PASSWORD = os.getenv('EMAIL_BOT_PASSWORD')

# for logs
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / '.data' / 'logs'

LOG_PATH.mkdir(parents=True, exist_ok=True)

LOG_PATH = LOG_PATH / 'bot.log'
