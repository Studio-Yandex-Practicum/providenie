import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_LEVEL = 'INFO'

EMAIL_BOT = os.getenv('EMAIL_BOT', 'FondProvidenieBot@yandex.ru')

# ЗАМЕНИТЬ НА МЫЛО КУРАТОРА ФОНДА
EMAIL_CURATOR = os.getenv('EMAIL_CURATOR', 'k.danilow2009@yandex.ru')
EMAIL_BOT_PASSWORD = os.getenv('EMAIL_BOT_PASSWORD', 'jyvsejdjxyixsxkh')
