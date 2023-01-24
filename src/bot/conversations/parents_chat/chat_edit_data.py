from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from .chat_show_data import chat_show_data
from bot import constants as const
from bot import keys as key
from bot import states


async def chat_select_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    if context.user_data[key.CURRENT_CHAT] == "Мамы ангелов":
        buttons = [
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_NAME,
                    callback_data=key.CHAT_PARENTS_NAME,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_PHONE,
                    callback_data=key.CHAT_PARENTS_PHONE,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.BTN_DONE, callback_data=str(key.END)
                )
            ],
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_NAME,
                    callback_data=key.CHAT_PARENTS_NAME,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_PHONE,
                    callback_data=key.CHAT_PARENTS_PHONE,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_NAME,
                    callback_data=key.CHAT_CHILD_NAME,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_BIRTHDAY,
                    callback_data=key.CHAT_CHILD_BIRTHDAY,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_PLACE_BIRTHDAY,
                    callback_data=key.CHAT_CHILD_PLACE_BIRTHDAY,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_TERM,
                    callback_data=key.CHAT_CHILD_TERM,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_WEIGHT,
                    callback_data=key.CHAT_CHILD_WEIGHT,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_HEIGHT,
                    callback_data=key.CHAT_CHILD_HEIGHT,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_DIAGNOSE,
                    callback_data=key.CHAT_CHILD_DIAGNOSE,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_CHILD_OPERATION,
                    callback_data=key.CHAT_CHILD_OPERATION,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.MSG_CHAT_EDIT_ABOUT_FOND,
                    callback_data=key.CHAT_ABOUT_FOND,
                )
            ],
            [
                InlineKeyboardButton(
                    text=const.BTN_DONE, callback_data=str(key.END)
                )
            ],
        ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(key.START_OVER)
    text = const.MSG_CHOOSE_TO_EDIT
    if not state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_markdown(text=text, reply_markup=keyboard)
    context.user_data[key.START_OVER] = True
    return states.CHAT_FEATURE


async def chat_edit_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод нового значения при редактировании данных."""
    context.user_data[key.CHAT_CURRENT_FEATURE] = update.callback_query.data
    text = const.MSG_ENTER_NEW_VALUE
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return states.CHAT_TYPING


async def chat_save_input(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.CHAT_FEATURES][user_data[key.CHAT_CURRENT_FEATURE]] = message
    user_data[key.START_OVER] = True
    return await chat_select_field(update, context)


async def chat_end_editing(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[key.START_OVER] = True
    await chat_show_data(update, context)
    return key.END
