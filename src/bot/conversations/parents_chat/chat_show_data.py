from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states


async def chat_show_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение всех введённых данных для вступления в чат"""
    user_data = context.user_data
    data = user_data.get(states.CHAT_FEATURES)
    if not data:
        text = "\nДанных нет.\n"
    else:
        text = (
            f'*ФИО родителя (опекуна):*\n  _{data.get(states.CHAT_PARENTS_NAME, "-")}_\n'
            f'*Номер телефона родителя(опекуна):*\n  _{data.get(states.CHAT_PARENTS_PHONE, "-")}_\n'
            f'*ФИО ребенка:*\n  _{data.get(states.CHAT_CHILD_NAME, "-")}_\n'
            f'*Дата рождения ребенка:*\n  _{data.get(states.CHAT_CHILD_BIRTHDAY, "-")}_\n'
            f'*Место рождения ребенка:*\n  _{data.get(states.CHAT_CHILD_PLACE_BIRTHDAY, "-")}_\n'
            f'*Срок беременности при рождении ребенка:*\n  _{data.get(states.CHAT_CHILD_TERM, "-")}_\n'
            f'*Вес при рождении:*\n  _{data.get(states.CHAT_CHILD_WEIGHT, "-")}_\n'
            f'*Рост при рождении:*\n  _{data.get(states.CHAT_CHILD_HEIGHT, "-")}_\n'
            f'*Диагнозы:*\n  _{data.get(states.CHAT_CHILD_DIAGNOSE, "-")}_\n'
            f'*Операции:*\n  _{data.get(states.CHAT_CHILD_OPERATION, "-")}_\n'
            f'*Дата обращения:*\n  _{data.get(states.CHAT_DATE_ADDRESS, "-")}_\n'
            f'*Как узнали о фонде:*\n  _{data.get(states.CHAT_ABOUT_FOND, "-")}_\n'
        )

    buttons = [
        [
            InlineKeyboardButton(
                text="Редактировать", callback_data=str(states.CHAT_DATA_EDIT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Отправить", callback_data=str(states.CHAT_SEND)
            )
        ],
        [
            InlineKeyboardButton(
                text="Список чатов", callback_data=str(states.END)
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(states.START_OVER)
    if state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard, parse_mode="Markdown"
        )
    else:
        await update.message.reply_markdown(text=text, reply_markup=keyboard)
    user_data[states.START_OVER] = False
    return states.CHAT_SHOWING
