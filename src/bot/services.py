from telegram.ext import ApplicationBuilder

from src.core.settings import TELEGRAM_TOKEN


def start_bot():
    """
    Функция инициализации бота.
    Отправляет объект бота в main.py.
    """
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    return application
