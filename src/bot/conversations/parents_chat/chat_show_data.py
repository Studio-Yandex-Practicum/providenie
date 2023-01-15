from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states


async def chat_show_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение всех введённых данных для вступления в чат"""
    user_data = context.user_data
    data = user_data.get(states.FEATURES)
    if not data:
        text = "\nДанных нет.\n"
    else:
        text = (
            f'<b>ФИО родителя (опекуна)</b>\n  <i>{data.get(states.CHAT_PARENTS_NAME, "-")}</i>\n'
            f'<b>Номер телефона родителя(опекуна)</b>\n  <i>{data.get(states.CHAT_PARENTS_PHONE, "-")}</i>\n'
            f'<b>ФИО ребенка</b>\n  <i>{data.get(states.CHAT_CHILD_NAME, "-")}</i>\n'
            f'<b>Дата рождения ребенка</b>\n  <i>{data.get(states.CHAT_CHILD_BIRTHDAY, "-")}</i>\n'
            f'<b>Место рождения ребенка</b>\n  <i>{data.get(states.CHAT_CHILD_PLACE_BIRTHDAY, "-")}</i>\n'
            f'<b>Срок беременности при рождении ребенка</b>\n  <i>{data.get(states.CHAT_CHILD_TERM, "-")}</i>\n'
            f'<b>Вес при рождении</b>\n  <i>{data.get(states.CHAT_CHILD_WEIGHT, "-")}</i>\n'
            f'<b>Рост при рождении</b>\n  <i>{data.get(states.CHAT_CHILD_HEIGHT, "-")}</i>\n'
            f'<b>Диагнозы</b>\n  <i>{data.get(states.CHAT_CHILD_DIAGNOSE, "-")}</i>\n'
            f'<b>Операции</b>\n  <i>{data.get(states.CHAT_CHILD_OPERATION, "-")}</i>\n'
            f'<b>Дата обращения</b>\n  <i>{data.get(states.CHAT_DATE_ADDRESS, "-")}</i>\n'
            f'<b>Как узнали о фонде</b>\n  <i>{data.get(states.CHAT_ABOUT_FOND, "-")}</i>\n'
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
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_html(text=text, reply_markup=keyboard)
    user_data[states.START_OVER] = False
    return states.CHAT_SHOWING
