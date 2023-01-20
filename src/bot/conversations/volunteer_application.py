from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state
from bot import templates
from bot.conversations.menu import start
from core.email import bot_send_email_to_curator


async def add_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Путь вступления в ряды волонтёров."""
    user_data = context.user_data
    user_data[key.START_OVER] = False
    text = const.MSG_NEED_INFORMATION
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_BEGIN, callback_data=str(key.VOLUNTEER)
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
    return state.ADDING_VOLUNTEER


async def adding_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем ФИО."""
    user_data = context.user_data
    user_data[key.FEATURES] = {key.LEVEL: key.VOLUNTEER}
    user_data[key.CURRENT_FEATURE] = key.NAME
    text = const.MSG_FULL_NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return state.ADDING_NAME


async def adding_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем ФИО, спрашиваем дату рождения."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.BIRTHDAY
    text = const.MSG_BIRTHDAY
    await update.message.reply_text(text=text)
    return state.ADDING_BIRTHDAY


async def adding_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату рождения, спрашиваем город проживания."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.CITY
    text = const.MSG_CITY
    await update.message.reply_text(text=text)
    return state.ADDING_CITY


async def adding_city(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем город проживания, спрашиваем номер телефона."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.PHONE
    text = const.MSG_PHONE
    await update.message.reply_text(text=text)
    return state.ADDING_PHONE


async def adding_phone(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем номер телефона, спрашиваем email."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.EMAIL
    text = const.MSG_EMAIL
    await update.message.reply_text(text=text)
    return state.ADDING_EMAIL


async def adding_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем email, спрашиваем вариант помощи."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.CURRENT_FEATURE] = key.MESSAGE
    text = const.MSG_YOUR_HELP_OPTION
    await update.message.reply_text(text=text)
    return state.ADDING_MESSAGE


async def adding_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем вариант помощи."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    return await show_volunteer(update, context)


async def skip_adding_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем пустой вариант помощи."""
    user_data = context.user_data
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = ""
    return await show_volunteer(update, context)


async def show_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение всех введённых данных волонтёра."""
    user_data = context.user_data
    data = user_data.get(key.FEATURES)
    full_name = data.get(key.NAME, "-")
    birthday = data.get(key.BIRTHDAY, "-")
    city = data.get(key.CITY, "-")
    phone = data.get(key.PHONE, "-")
    email = data.get(key.EMAIL, "-")
    message = data.get(key.MESSAGE, "-")
    if not data:
        text = const.MSG_NO_DATA
    else:
        text = templates.MSG_VOLUNTEER_DATA.format(
            full_name, birthday, city, phone, email, message
        )
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_EDIT, callback_data=str(key.EDIT_VOLUNTEER)
            ),
            InlineKeyboardButton(
                text=const.BTN_SEND, callback_data=str(key.SEND_VOLUNTEER)
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
    return state.SHOWING_VOLUNTEER


async def select_volunteer_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_FULL_NAME, callback_data=str(key.NAME)
            ),
            InlineKeyboardButton(
                text=const.BTN_BIRTHDAY, callback_data=str(key.BIRTHDAY)
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_CITY, callback_data=str(key.CITY)
            ),
            InlineKeyboardButton(
                text=const.BTN_PHONE, callback_data=str(key.PHONE)
            ),
            InlineKeyboardButton(
                text=const.BTN_EMAIL, callback_data=str(key.EMAIL)
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_YOUR_HELP_OPTION,
                callback_data=str(key.MESSAGE),
            ),
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
    return state.VOLUNTEER_FEATURE


async def ask_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод нового значения, при редактировании данных."""
    context.user_data[key.CURRENT_FEATURE] = update.callback_query.data
    text = const.MSG_ENTER_NEW_VALUE
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return state.TYPING_VOLUNTEER


async def save_volunteer_input(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения, при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = message
    user_data[key.START_OVER] = True
    return await select_volunteer_field(update, context)


async def end_editing(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[key.START_OVER] = True
    await show_volunteer(update, context)
    return key.END


async def end_sending(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение в главное меню после отправки письма."""
    context.user_data[key.START_OVER] = True
    await start(update, context)
    return state.STOPPING


async def send_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка письма куратору."""
    user_data = context.user_data
    data = user_data.get(key.FEATURES)
    name = data.get(key.NAME, "-")
    birthday = data.get(key.BIRTHDAY, "-")
    city = data.get(key.CITY, "-")
    phone = data.get(key.PHONE, "-")
    email = data.get(key.EMAIL, "-")
    message = data.get(key.MESSAGE, "-")
    subject = templates.VOLUNTEER_DATA_SUBJECT
    html = templates.HTML_VOLUNTEER_DATA.format(
        subject, name, birthday, city, phone, email, message
    )

    func = bot_send_email_to_curator(subject, html)
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
    return state.VOLUNTEER_SENT
