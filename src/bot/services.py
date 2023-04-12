from telegram.ext import Application

from bot.core.logger import logger  # noqa
from bot.core.settings import settings
from bot.error_handler import error_handler
from bot.handlers import main_menu_handler


def init_bot():
    """Initialize a Telegram bot application with a main menu handler."""
    application = Application.builder().token(settings.telegram_token).build()
    application.add_handler(main_menu_handler)
    application.add_error_handler(error_handler)
    return application
