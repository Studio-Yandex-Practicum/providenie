from telegram.ext import Application

from bot.handlers import main_menu_handler
from bot.core.settings import settings
from bot.core.logger import logger  # noqa


def init_bot():
    """Initialize a Telegram bot application with a main menu handler"""

    application = Application.builder().token(settings.telegram_token).build()
    application.add_handler(main_menu_handler)
    return application
