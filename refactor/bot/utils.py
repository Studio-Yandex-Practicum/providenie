from typing import Optional

from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup, Update

from bot.constants import key
from bot.constants.info.text import MESSAGE_MARKDOWN


async def send_message(
    update: Update,
    text: str,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    link_preview: bool = False
):
    """Send a message with optional inline keyboard and link preview"""

    message_args = {
        'text': text,
        'reply_markup': keyboard,
        'parse_mode': MESSAGE_MARKDOWN,
        'disable_web_page_preview': not link_preview,
    }
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.edit_text(**message_args)
    else:
        await update.message.reply_text(**message_args)


def get_menu_buttons(menu: dict):
    """Generate inline keyboard buttons for menu"""

    return [
        [Button(text=option.get(key.BUTTON_TEXT), callback_data=callback)]
        for callback, option in menu.items()
    ]
