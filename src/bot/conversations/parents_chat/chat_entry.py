from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import dictionaries as dict
from bot import keys as key
from bot import states as state


async def enter_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    chat = update.callback_query.data
    user_data = context.user_data
    user_data[key.CURRENT_CHAT] = chat
    text = f'{dict.CHAT_DESCRIPTION[chat]["description"]}'
    user_data[key.CURRENT_CHAT] = dict.CHAT_DESCRIPTION[chat]["name"]

    buttons = [
        [
            InlineKeyboardButton(
                text=const.MSG_CHAT_ENTER, callback_data=key.ENTRY_CHAT
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_BACK,
                callback_data=key.CHATS,
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BIN_MAIN_MENU, callback_data=str(key.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return state.ENTERING_CHAT
