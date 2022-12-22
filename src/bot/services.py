from conversations.menu import start
from telegram.ext import ApplicationBuilder, CommandHandler

from src.core.settings import TELEGRAM_TOKEN


def start_bot():
    """Функция инициализации и запуска бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
