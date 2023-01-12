import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.error import Forbidden, TelegramError
from telegram.ext import ApplicationBuilder

from bot import constants as const
from bot.handlers.handler import conv_handler
from core.settings import TELEGRAM_TOKEN


def start_bot():
    """Функция инициализации и запуска бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(conv_handler)
    return application


async def reply_message(
    update: Update, text: str, reply_markup: InlineKeyboardMarkup
) -> None:
    """Функция отправляет сообщение в Telegram чат."""
    try:
        message = update.message
        await message.reply_markdown_v2(text=text, reply_markup=reply_markup)
    except Forbidden:
        logging.error(const.LOG_BOT_BLOCKED_BY_USER)
    except TelegramError:
        logging.error(const.LOG_ERROR_IN_RESPONSE)
