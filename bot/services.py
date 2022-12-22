from telegram import InlineKeyboardMarkup, Update
from telegram.error import Forbidden, TelegramError

from core.logger import logger


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
