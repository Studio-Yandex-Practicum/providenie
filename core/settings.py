import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_LEVEL = 'INFO'

TEXT_START_BUTTON = """
    Привет! Я бот-помощник Фонда помощи недоношенным детям и их семьям «Провидение».
    Мы  спасаем зрение недоношенным детям!
    Я помогу вам узнать как получить и оказать помощь.
"""
