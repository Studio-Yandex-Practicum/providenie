from typing import Optional
from telegram import Update, InlineKeyboardMarkup


async def send_message(
    update: Update,
    message: str,
    keyboard: Optional[InlineKeyboardMarkup] = None
):
    MESSAGE_MARKDOWN = 'HTML'
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.edit_text(message, reply_markup=keyboard, parse_mode=MESSAGE_MARKDOWN)
    else:
        await update.message.reply_text(message, reply_markup=keyboard, parse_mode=MESSAGE_MARKDOWN)
