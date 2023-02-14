from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state
from bot import templates
from bot.conversations.main_menu import start
from core.email import bot_send_email_to_curator


async def chat_end_sending(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение в главное меню после отправки письма."""
    context.user_data[key.START_OVER] = True
    await start(update, context)
    return state.STOPPING


async def chat_send_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка письма куратору."""

    user_data = context.user_data
    data = user_data.get(key.CHAT_FEATURES)
    chat_data = dict(
        subject=templates.CHAT_DATA_SUBJECT,
        current_chat=user_data.get(key.CURRENT_CHAT, "-"),
        chat_parents_name=data.get(key.CHAT_PARENTS_NAME, "-"),
        chat_parents_phone=data.get(key.CHAT_PARENTS_PHONE, "-"),
        chat_child_name=data.get(key.CHAT_CHILD_NAME, "-"),
        chat_child_birthday=data.get(key.CHAT_CHILD_BIRTHDAY, "-"),
        chat_child_place_birthday=data.get(key.CHAT_CHILD_PLACE_BIRTHDAY, "-"),
        chat_child_term=data.get(key.CHAT_CHILD_TERM, "-"),
        chat_child_weight=data.get(key.CHAT_CHILD_WEIGHT, "-"),
        chat_child_height=data.get(key.CHAT_CHILD_HEIGHT, "-"),
        chat_child_diagnose=data.get(key.CHAT_CHILD_DIAGNOSE, "-"),
        chat_child_operation=data.get(key.CHAT_CHILD_OPERATION, "-"),
        chat_about_fond=data.get(key.CHAT_ABOUT_FOND, "-"),
        date_address=date.today(),
    )
    if user_data[key.CURRENT_CHAT] == "Мамы ангелов":
        html = templates.HTML_CHAT_ANGELS_DATA.format(*chat_data.values())
    elif user_data[key.CURRENT_CHAT] == "Бабушки торопыжек":
        html = templates.HTML_CHAT_GRANDMOTHERS_DATA.format(
            *chat_data.values()
        )
    else:
        html = templates.HTML_CHAT_DATA.format(*chat_data.values())
    func = bot_send_email_to_curator(chat_data["subject"], html)
    if func:
        return_text = const.MSG_REQUEST_SENT
        return_text += "\n<контакты куратора-волонтёра для связи>"
    else:
        return_text = const.MSG_SENDING_ERROR
    button = InlineKeyboardButton(
        text=const.BTN_BACK, callback_data=str(key.SENT)
    )
    keyboard = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=keyboard
    )
    return state.CHAT_SEND
