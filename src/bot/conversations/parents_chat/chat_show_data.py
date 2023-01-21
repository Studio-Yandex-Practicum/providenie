from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states, templates


async def chat_show_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение всех введённых данных для вступления в чат"""
    user_data = context.user_data
    data = user_data.get(key.CHAT_FEATURES)
    chat_data = dict(
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
    if not data:
        text = const.MSG_NO_DATA
    elif user_data[key.CURRENT_CHAT] == "Мамы ангелов":
        text = templates.MSG_CHAT_ANGELS_DATA.format(
            chat_data["chat_parents_name"], chat_data["chat_parents_phone"]
        )
    elif user_data[key.CURRENT_CHAT] == "Бабушки торопыжек":
        text = templates.MSG_CHAT_GRANDMOTHERS_DATA.format(*chat_data.values())
    else:
        text = templates.MSG_CHAT_DATA.format(*chat_data.values())

    buttons = [
        [
            InlineKeyboardButton(
                text="Редактировать", callback_data=states.CHAT_DATA_EDIT
            )
        ],
        [
            InlineKeyboardButton(
                text="Отправить", callback_data=states.CHAT_SEND
            )
        ],
        [
            InlineKeyboardButton(
                text="Главное меню", callback_data=str(key.END)
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(key.START_OVER)
    if state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard, parse_mode="html"
        )
    else:
        await update.message.reply_text(
            text=text, reply_markup=keyboard, parse_mode="html"
        )
    user_data[key.START_OVER] = False
    return states.CHAT_SHOWING
