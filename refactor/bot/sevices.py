from telegram.ext import Application

from core import settings
from core.logger import logger  # noqa
from bot.handlers import main_menu_handler


def init_bot():
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(main_menu_handler)
    return application
