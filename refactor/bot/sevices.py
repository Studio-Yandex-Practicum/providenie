from telegram.ext import Application

from bot.handlers import main_menu_handler
from core import settings
from core.logger import logger  # noqa


def init_bot():
    """Initialize a Telegram bot application with a main menu handler"""

    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(main_menu_handler)
    return application
