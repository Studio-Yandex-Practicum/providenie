from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state
from bot import services as service
from bot import templates


async def ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Возможность задать вопрос."""
    user_data = context.user_data
    user_data[key.START_OVER] = False
    text = const.MSG_QUESTION_NEED_INFORMATION
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
        text=text, reply_markup=keyboard
    )
    return state.ASKING_QUESTION


async def asking_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем имя."""
    user_data = context.user_data
    user_data[key.FEATURES] = {key.LEVEL: key.QUESTION}
    user_data[key.CURRENT_FEATURE] = key.NAME
    text = const.MSG_NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return state.ADDING_NAME


async def adding_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем имя, спрашиваем тему вопроса."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.THEME
    text = const.MSG_THEME
    await update.message.reply_text(text=text)
    return state.ADDING_THEME


async def adding_theme(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем тему вопроса, спрашиваем содержание вопроса."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.QUESTION
    text = const.MSG_QUESTION
    await update.message.reply_text(text=text)
    return state.ADDING_QUESTION


async def adding_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем содержание вопроса."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    return await show_question(update, context)


async def show_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение вопроса."""
    user_data = context.user_data
    data = user_data.get(key.FEATURES)
    full_name = data.get(key.NAME, "-")
    theme = data.get(key.THEME, "-")
    question = data.get(key.QUESTION, "-")
    if not data:
        text = const.MSG_NO_DATA
    else:
        text = templates.MSG_QUESTION_DATA.format(full_name, theme, question)
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


async def select_question_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_NAME, callback_data=key.NAME
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_THEME, callback_data=key.THEME
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
    text = const.MSG_CHOOSE_TO_EDIT
    if not context.user_data.get(key.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)
    context.user_data[key.START_OVER] = True
    return state.QUESTION_FEATURE


async def ask_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Ввод нового значения, при редактировании данных."""
    context.user_data[key.CURRENT_FEATURE] = update.callback_query.data
    text = const.MSG_ENTER_NEW_VALUE
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return state.TYPING_QUESTION


async def save_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сохранение нового значения, при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.START_OVER] = True
    return await select_question_field(update, context)


async def end_editing(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[key.START_OVER] = True
    await show_question(update, context)
    return key.END


async def send_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отправка вопроса куратору."""
    user_data = context.user_data
    data = user_data.get(key.FEATURES)
    full_name = data.get(key.NAME, "-")
    theme = data.get(key.THEME, "-")
    question = data.get(key.QUESTION, "-")
    current_user_id = update.effective_chat.id
    text = templates.MSG_QUESTION_TO_CURATOR.format(full_name, theme, question)
    user_url = f"tg://user?id={current_user_id}"
    button = InlineKeyboardButton(text=const.BTN_ANSWER, url=user_url)
    reply_markup = InlineKeyboardMarkup.from_button(button)
    sent = await service.send_message_to_curator(
        context=context,
        message=text,
        reply_markup=reply_markup,
        parse_mode="html",
    )
    if sent:
        return_text = const.MSG_QUESTION_SENT
    else:
        return_text = const.MSG_QUESTION_ERROR_SENT

    button = InlineKeyboardButton(
        text=const.BTN_BACK, callback_data=key.SENT
    )
    reply_markup = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=reply_markup
    )
    return state.QUESTION_SENT
