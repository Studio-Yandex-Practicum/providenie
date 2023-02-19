from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state
from bot import templates
from core.email import bot_send_email_to_curator


async def enter_submenu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Возможность задать вопрос."""
    user_data = context.user_data
    user_data[key.START_OVER] = False
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_BEGIN, callback_data=key.QUESTION
            ),
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.END)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_QUESTION_NEED_INFORMATION, reply_markup=keyboard
    )
    return state.ASKING_QUESTION


async def ask_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем имя."""
    user_data = context.user_data
    user_data[key.FEATURES] = {key.LEVEL: key.QUESTION}
    user_data[key.CURRENT_FEATURE] = key.NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=const.MSG_NAME)
    return state.ADDING_NAME


async def save_feature(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    next_feature: Optional[str] = None,
    reply_text: Optional[str] = None,
):
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    if next_feature:
        user_data[key.CURRENT_FEATURE] = next_feature
    if reply_text:
        await update.message.reply_text(text=reply_text)


async def ask_phone_number(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем имя, спрашиваем номер телефона."""
    await save_feature(update, context, key.PHONE, const.MSG_PHONE)
    return state.ADDING_PHONE


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сохраняем номер телефона, спрашиваем email."""
    await save_feature(update, context, key.EMAIL, const.MSG_EMAIL)
    return state.ADDING_EMAIL


async def ask_question_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем email, спрашиваем содержание вопроса."""
    await save_feature(update, context, key.QUESTION, const.MSG_QUESTION)
    return state.ADDING_QUESTION


async def save_question_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем содержание вопроса."""
    await save_feature(update, context)
    return await display_entered_values(update, context)


async def display_entered_values(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение вопроса."""
    user_data = context.user_data
    data = user_data.get(key.FEATURES)
    name = data.get(key.NAME, "-")
    phone = data.get(key.PHONE, "-")
    email = data.get(key.EMAIL, "-")
    question = data.get(key.QUESTION, "-")
    if not data:
        text = const.MSG_NO_DATA
    else:
        text = templates.MSG_QUESTION_DATA.format(name, phone, email, question)
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_EDIT, callback_data=key.EDIT_QUESTION
            ),
            InlineKeyboardButton(
                text=const.BTN_SEND, callback_data=key.SEND_QUESTION
            ),
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.END)
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if user_data.get(key.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            parse_mode="html", text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            parse_mode="html", text=text, reply_markup=keyboard
        )
    user_data[key.START_OVER] = False
    return state.SHOWING_QUESTION


async def display_editing_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    buttons = [
        [
            InlineKeyboardButton(text=const.BTN_NAME, callback_data=key.NAME),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_PHONE, callback_data=key.PHONE
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_EMAIL, callback_data=key.EMAIL
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_QUESTION, callback_data=key.QUESTION
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_DONE, callback_data=str(key.END)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if not context.user_data.get(key.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=const.MSG_CHOOSE_TO_EDIT, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text=const.MSG_CHOOSE_TO_EDIT, reply_markup=keyboard
        )
    context.user_data[key.START_OVER] = True
    return state.QUESTION_FEATURE


async def ask_new_value(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод нового значения, при редактировании данных."""
    context.user_data[key.CURRENT_FEATURE] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_ENTER_NEW_VALUE
    )
    return state.TYPING_QUESTION


async def save_new_value(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения, при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.START_OVER] = True
    return await display_editing_menu(update, context)


async def display_edited_values(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[key.START_OVER] = True
    await display_entered_values(update, context)
    return key.END


async def send_values_to_curator(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отправка вопроса куратору."""
    user_data = context.user_data
    data = user_data.get(key.FEATURES)
    name = data.get(key.NAME, "-")
    phone = data.get(key.PHONE, "-")
    email = data.get(key.EMAIL, "-")
    question = data.get(key.QUESTION, "-")

    subject = templates.ASK_QUESTION_SUBJECT
    html = templates.HTML_ASK_QUESTION_DATA.format(
        subject, name, phone, email, question
    )
    func = bot_send_email_to_curator(subject, html)
    if func:
        return_text = const.MSG_RESPONSE_ASK_QUESTION
    else:
        return_text = const.MSG_SENDING_ERROR
    button = InlineKeyboardButton(text=const.BTN_BACK, callback_data=key.SENT)
    keyboard = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=keyboard
    )
    return state.VOLUNTEER_SENT

    # current_user_id = update.effective_chat.id
    # user_url = f"tg://user?id={current_user_id}"
    # button = InlineKeyboardButton(text=const.BTN_ANSWER, url=user_url)

    # text = templates.MSG_QUESTION_TO_CURATOR.format(full_name, theme, question)
    # reply_markup = InlineKeyboardMarkup.from_button(button)

    # sent = await service.send_message_to_curator(
    #     context=context,
    #     message=text,
    #     reply_markup=reply_markup,
    #     parse_mode="html",
    # )
    # if sent:
    #     return_text = const.MSG_QUESTION_SENT
    # else:
    #     return_text = const.MSG_QUESTION_ERROR_SENT

    # button = InlineKeyboardButton(text=const.BTN_BACK, callback_data=key.SENT)
    # reply_markup = InlineKeyboardMarkup.from_button(button)
    # await update.callback_query.answer()
    # await update.callback_query.edit_message_text(
    #     text=return_text, reply_markup=reply_markup
    # )
    # return state.QUESTION_SENT
