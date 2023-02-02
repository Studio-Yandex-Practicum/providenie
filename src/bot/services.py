import logging

from telegram import InlineKeyboardMarkup
from telegram.error import Forbidden, TelegramError
from telegram.ext import ApplicationBuilder, ContextTypes

from bot import constants as const
from bot.handlers.handler import conv_handler
from core.settings import TELEGRAM_CURATOR, TELEGRAM_TOKEN


def start_bot():
    """Функция инициализации и запуска бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(conv_handler)
    return application


async def send_message_to_curator(
    context: ContextTypes.DEFAULT_TYPE,
    message: str,
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = None,
) -> bool:
    """Отправляем сообщение куратору в Telegram."""
    try:
        await context.bot.send_message(
            chat_id=TELEGRAM_CURATOR,
            text=message,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
        return True
    except Forbidden:
        logging.error(const.LOG_BOT_BLOCKED_BY_USER)
    except TelegramError as error:
        logging.error(error)
    return False
