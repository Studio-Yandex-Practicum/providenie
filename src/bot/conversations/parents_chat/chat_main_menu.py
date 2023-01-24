from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import keys as key
from bot import states as state


async def select_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Выбрать чат"""

    buttons_chat = [
        [
            InlineKeyboardButton(
                text="Дети, рожде‌нные раньше срока (до 1,5)",
                callback_data=str(key.CHAT_BABY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Дети, рожде‌нные раньше срока (от 1,5)",
                callback_data=str(key.CHAT_CHILD),
            )
        ],
        [
            InlineKeyboardButton(
                text="Ретинопатия", callback_data=str(key.CHAT_RETINOPATIA)
            )
        ],
        [
            InlineKeyboardButton(
                text="Шунтята", callback_data=str(key.CHAT_SHUNTATA)
            )
        ],
        [
            InlineKeyboardButton(
                text="Бабушки торопыжек",
                callback_data=str(key.CHAT_GRANDMOTHERS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Отвести душу и поплакать",
                callback_data=str(key.CHAT_CRY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Мамы ангелов", callback_data=str(key.CHAT_ANGELS)
            )
        ],
        [
            InlineKeyboardButton(
                text="Ретинопатия недоношенных 4-5 стадии",
                callback_data=str(key.CHAT_RETINOPATIA_4_5),
            )
        ],
        [
            InlineKeyboardButton(
                text="Дети с офтальмологическими проблемами",
                callback_data=str(key.CHAT_PROBLEMS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Реабилитация зрения",
                callback_data=str(key.CHAT_REHABILITATION),
            )
        ],
        [
            InlineKeyboardButton(
                text="«Семьи торопыжек» t.me/toropizhki",
                callback_data=str(key.CHAT_TELEGRAM),
            )
        ],
        [
            InlineKeyboardButton(
                text="Возврат в главное меню", callback_data=str(key.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons_chat)
    text = "Выберите чат для вступления:"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return state.SELECTING_CHAT
