from telegram import ReplyKeyboardMarkup, Update


async def reply_message(
        update: Update,
        text: str,
        reply_markup: ReplyKeyboardMarkup
) -> None:
    """Функция отправляет сообщение в Telegram чат."""
    message = update.message
    await message.reply_markdown_v2(text=text, reply_markup=reply_markup)
