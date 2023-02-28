from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import dictionaries as dict
from bot import keys as key
from bot import states as state


async def select_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Выбрать чат"""

    buttons_chat = [
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_BABY]["shortname"],
                callback_data=str(key.CHAT_BABY),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_CHILD]["shortname"],
                callback_data=str(key.CHAT_CHILD),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_RETINOPATIA]["shortname"],
                callback_data=str(key.CHAT_RETINOPATIA),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_SHUNTATA]["name"],
                callback_data=str(key.CHAT_SHUNTATA),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_GRANDMOTHERS]["name"],
                callback_data=str(key.CHAT_GRANDMOTHERS),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_CRY]["name"],
                callback_data=str(key.CHAT_CRY),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_ANGELS]["name"],
                callback_data=str(key.CHAT_ANGELS),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_RETINOPATIA_4_5]["name"],
                callback_data=str(key.CHAT_RETINOPATIA_4_5),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_PROBLEMS]["name"],
                callback_data=str(key.CHAT_PROBLEMS),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_REHABILITATION]["name"],
                callback_data=str(key.CHAT_REHABILITATION),
            )
        ],
        [
            InlineKeyboardButton(
                text=dict.CHAT_DESCRIPTION[key.CHAT_TELEGRAM]["name"],
                callback_data=str(key.CHAT_TELEGRAM),
            )
        ],
        [
            InlineKeyboardButton(
                const.BIN_MAIN_MENU, callback_data=str(key.END)
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
