from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states
from bot.conversations.menu import start
from core.email import bot_send_email_to_curator


(
    START_OVER,
    STOPPING,
    END,
    CHAT_FEATURE,
    CURRENT_CHAT,
    SELECTING_CHAT,
    FEATURES,
    CURRENT_FEATURE,
    ENTRY_CHAT,
    ENTERING_CHAT,
    CHAT_TYPING,
    CHAT_SHOWING,
    CHAT_DATA_EDIT,
    CHAT_SEND,
) = map(chr, range(120, 134))

(
    CHAT_PARENTS_NAME,
    CHAT_PARENTS_PHONE,
    CHAT_CHILD_NAME,
    CHAT_CHILD_BIRTHDAY,
    CHAT_CHILD_PLACE_BIRTHDAY,
    CHAT_CHILD_TERM,
    CHAT_CHILD_WEIGHT,
    CHAT_CHILD_HEIGHT,
    CHAT_CHILD_DIAGNOSE,
    CHAT_CHILD_OPERATION,
    CHAT_DATE_ADDRESS,
    CHAT_ABOUT_FOND,
) = map(chr, range(140, 153))


async def send_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка письма куратору."""

    user_data = context.user_data
    data = user_data.get(states.FEATURES)
    chat_parents_name = data.get(states.CHAT_PARENTS_NAME, "-")
    chat_parents_phone = data.get(states.states.CHAT_PARENTS_PHONE, "-")
    chat_child_name = data.get(states.CHAT_CHILD_NAME, "-")
    chat_child_birthday = data.get(states.states.CHAT_CHILD_BIRTHDAY, "-")
    chat_place_birthday = data.get(
        states.states.CHAT_CHILD_PLACE_BIRTHDAY, "-"
    )
    chat_child_term = data.get(states.states.CHAT_CHILD_TERM, "-")
    chat_child_weight = data.get(states.CHAT_CHILD_WEIGHT, "-")
    chat_child_height = data.get(states.states.CHAT_CHILD_HEIGHT, "-")
    chat_child_diagnose = data.get(states.CHAT_CHILD_DIAGNOSE, "-")
    chat_child_operation = data.get(states.states.CHAT_CHILD_OPERATION, "-")
    chat_date_address = data.get(states.CHAT_DATE_ADDRESS, "-")
    chat_about_fond = data.get(states.states.CHAT_ABOUT_FOND, "-")
    subject = "Вступление в чат"
    html = f"""
        <html>
            <body>
                <h1>{subject}</h1>
                <p>
                    <b>ФИО родителя(опекуна):</b> {chat_parents_name}<br/>
                    <b>Телефон родителя(опекуна):</b> {chat_parents_phone}<br/>
                    <b>ФИО ребенка:</b> {chat_child_name}<br/>
                    <b>Дата рождения:</b> {chat_child_birthday}<br/>
                    <b>Место рождения:</b> {chat_place_birthday}<br/>
                    <b>Срок беременности при рождении:</b> {chat_child_term}
                    <b>Вес при рождении:</b> {chat_child_weight}<br/>
                    <b>Рост при рождении:</b> {chat_child_height}<br/>
                    <b>Дигнозы:</b> {chat_child_diagnose}<br/>
                    <b>Операции ребенка:</b> {chat_child_operation}<br/>
                    <b>Дата обращения:</b> {chat_date_address}<br/>
                    <b>Как узнали о фонде:</b> {chat_about_fond}
                </p>
            </body>
        </html>
    """

    func = bot_send_email_to_curator(subject, html)
    if func:
        return_text = (
            "Ваша заявка отправлена.\n"
            "<контакты куратора-волонтёра для связи>"
        )
    else:
        return_text = "Ошибка отправки email куратору!"
    button = InlineKeyboardButton(
        text="Назад", callback_data=str(states.CHAT_SEND)
    )
    keyboard = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=keyboard
    )
    return states.CHAT_SEND


async def end_sending(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение в главное меню после отправки письма."""
    context.user_data[states.START_OVER] = True
    await start(update, context)
    return states.STOPPING
