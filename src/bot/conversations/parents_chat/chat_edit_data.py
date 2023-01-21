from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from .chat_show_data import chat_show_data
from bot import keys, states


async def chat_select_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    if context.user_data[keys.CURRENT_CHAT] == "Мамы ангелов":
        buttons = [
            [
                InlineKeyboardButton(
                    text="ФИО мамы(папы)",
                    callback_data=keys.CHAT_PARENTS_NAME,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Телефон мамы(папы)",
                    callback_data=keys.CHAT_PARENTS_PHONE,
                )
            ],
            [InlineKeyboardButton(text="Готово", callback_data=str(keys.END))],
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    text="ФИО родителя(опекуна)",
                    callback_data=keys.CHAT_PARENTS_NAME,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Телефон родителя",
                    callback_data=keys.CHAT_PARENTS_PHONE,
                )
            ],
            [
                InlineKeyboardButton(
                    text="ФИО ребенка",
                    callback_data=keys.CHAT_CHILD_NAME,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Дата рождения ребенка",
                    callback_data=keys.CHAT_CHILD_BIRTHDAY,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Место рождения ребенка",
                    callback_data=keys.CHAT_CHILD_PLACE_BIRTHDAY,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Срок беременности при рождении",
                    callback_data=keys.CHAT_CHILD_TERM,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вес ребенка при рождении",
                    callback_data=keys.CHAT_CHILD_WEIGHT,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Рост ребенка при рождении",
                    callback_data=keys.CHAT_CHILD_HEIGHT,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Диагнозы",
                    callback_data=keys.CHAT_CHILD_DIAGNOSE,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Операции",
                    callback_data=keys.CHAT_CHILD_OPERATION,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Как узнали о фонде",
                    callback_data=keys.CHAT_ABOUT_FOND,
                )
            ],
            [InlineKeyboardButton(text="Готово", callback_data=str(keys.END))],
        ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(keys.START_OVER)
    text = "Выберите для редактирования:"
    if not state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_markdown(text=text, reply_markup=keyboard)
    context.user_data[keys.START_OVER] = True
    return states.CHAT_FEATURE


async def chat_edit_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод нового значения при редактировании данных."""
    context.user_data[states.CHAT_CURRENT_FEATURE] = update.callback_query.data
    text = "Введите новое значение:"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return states.CHAT_TYPING


async def chat_save_input(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[keys.CHAT_FEATURES][
        user_data[keys.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.START_OVER] = True
    return await chat_select_field(update, context)


async def chat_end_editing(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[keys.START_OVER] = True
    await chat_show_data(update, context)
    return str(keys.END)
