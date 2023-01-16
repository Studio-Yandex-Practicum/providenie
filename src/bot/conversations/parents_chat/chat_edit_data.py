from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from .chat_show_data import chat_show_data
from bot import states


async def select_chat_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""

    buttons = [
        [
            InlineKeyboardButton(
                text="ФИО родителя(опекуна).",
                callback_data=str(states.CHAT_PARENTS_NAME),
            )
        ],
        [
            InlineKeyboardButton(
                text="Телефон родителя",
                callback_data=str(states.CHAT_PARENTS_PHONE),
            )
        ],
        [
            InlineKeyboardButton(
                text="ФИО ребенка", callback_data=str(states.CHAT_CHILD_NAME)
            )
        ],
        [
            InlineKeyboardButton(
                text="Дата рождения ребенка",
                callback_data=str(states.CHAT_CHILD_BIRTHDAY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Место рождения ребенка",
                callback_data=str(states.CHAT_CHILD_PLACE_BIRTHDAY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Срок беременности при рождении ребенка",
                callback_data=str(states.CHAT_CHILD_TERM),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вес ребенка при рождении",
                callback_data=str(states.CHAT_CHILD_WEIGHT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Рост ребенка при рождении",
                callback_data=str(states.CHAT_CHILD_HEIGHT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Диагнозы", callback_data=str(states.CHAT_CHILD_DIAGNOSE)
            )
        ],
        [
            InlineKeyboardButton(
                text="Операции", callback_data=str(states.CHAT_CHILD_OPERATION)
            )
        ],
        [
            InlineKeyboardButton(
                text="Дата обращения",
                callback_data=str(states.CHAT_DATE_ADDRESS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Как узнали о фонде",
                callback_data=str(states.CHAT_ABOUT_FOND),
            )
        ],
        [InlineKeyboardButton(text="Готово", callback_data=str(states.END))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(states.START_OVER)
    text = "Выберите для редактирования:"
    if not state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_markdown(text=text, reply_markup=keyboard)
    context.user_data[states.START_OVER] = True
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


async def save_chat_input(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.START_OVER] = True
    return await select_chat_field(update, context)


async def chat_end_editing(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[states.START_OVER] = True
    await chat_show_data(update, context)
    return states.END
