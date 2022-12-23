from telegram import InlineKeyboardMarkup, Update
from telegram.error import Forbidden, TelegramError
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.conversations.menu import start
from core.logger import logger
from core.settings import TELEGRAM_TOKEN


def start_bot():
    """Функция инициализации и запуска бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    return application


async def reply_message(
    update: Update, text: str, reply_markup: InlineKeyboardMarkup
) -> None:
    """Функция отправляет сообщение в Telegram чат."""
    try:
        message = update.message
        await message.reply_markdown_v2(text=text, reply_markup=reply_markup)
    except Forbidden:
        logger.error("Бот заблокирован пользователем")
    except TelegramError:
        logger.error("Ошибка при ответе на сообщение")
