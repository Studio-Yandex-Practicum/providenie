from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import states, templates
from bot.conversations.menu import start
from core.email import bot_send_email_to_curator


async def add_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Путь вступления в ряды волонтёров."""
    user_data = context.user_data
    user_data[states.START_OVER] = False
    text = const.MSG_NEED_INFORMATION
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_BEGIN, callback_data=str(states.VOLUNTEER)
            ),
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(states.END)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )
    return states.ADDING_VOLUNTEER


async def adding_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем ФИО."""
    user_data = context.user_data
    user_data[states.FEATURES] = {states.LEVEL: states.VOLUNTEER}
    user_data[states.CURRENT_FEATURE] = states.NAME
    text = const.MSG_FULL_NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return states.ADDING_NAME


async def adding_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем ФИО, спрашиваем дату рождения."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.BIRTHDAY
    text = const.MSG_BIRTHDAY
    await update.message.reply_text(text=text)
    return states.ADDING_BIRTHDAY


async def adding_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату рождения, спрашиваем город проживания."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CITY
    text = const.MSG_CITY
    await update.message.reply_text(text=text)
    return states.ADDING_CITY


async def adding_city(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем город проживания, спрашиваем номер телефона."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.PHONE
    text = const.MSG_PHONE
    await update.message.reply_text(text=text)
    return states.ADDING_PHONE


async def adding_phone(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем номер телефона, спрашиваем email."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.EMAIL
    text = const.MSG_EMAIL
    await update.message.reply_text(text=text)
    return states.ADDING_EMAIL


async def adding_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем email, спрашиваем вариант помощи."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.MESSAGE
    text = const.MSG_YOUR_HELP_OPTION
    await update.message.reply_text(text=text)
    return states.ADDING_MESSAGE


async def adding_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем вариант помощи."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    return await show_volunteer(update, context)


async def skip_adding_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем пустой вариант помощи."""
    user_data = context.user_data
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = ""
    return await show_volunteer(update, context)


async def show_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение всех введённых данных волонтёра."""
    user_data = context.user_data
    data = user_data.get(states.FEATURES)
    full_name = data.get(states.NAME, "-")
    birthday = data.get(states.BIRTHDAY, "-")
    city = data.get(states.CITY, "-")
    phone = data.get(states.PHONE, "-")
    email = data.get(states.EMAIL, "-")
    message = data.get(states.MESSAGE, "-")
    if not data:
        text = const.MSG_NO_DATA
    else:
        text = templates.MSG_VOLUNTEER_DATA.format(
            full_name, birthday, city, phone, email, message
        )
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_EDIT, callback_data=str(states.EDIT_VOLUNTEER)
            ),
            InlineKeyboardButton(
                text=const.BTN_SEND, callback_data=str(states.SEND_VOLUNTEER)
            ),
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(states.END)
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = user_data.get(states.START_OVER)
    if state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            parse_mode="html", text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            parse_mode="html", text=text, reply_markup=keyboard
        )
    user_data[states.START_OVER] = False
    return states.SHOWING_VOLUNTEER


async def select_volunteer_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_FULL_NAME, callback_data=str(states.NAME)
            ),
            InlineKeyboardButton(
                text=const.BTN_BIRTHDAY, callback_data=str(states.BIRTHDAY)
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_CITY, callback_data=str(states.CITY)
            ),
            InlineKeyboardButton(
                text=const.BTN_PHONE, callback_data=str(states.PHONE)
            ),
            InlineKeyboardButton(
                text=const.BTN_EMAIL, callback_data=str(states.EMAIL)
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_YOUR_HELP_OPTION,
                callback_data=str(states.MESSAGE),
            ),
            InlineKeyboardButton(
                text=const.BTN_DONE, callback_data=str(states.END)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(states.START_OVER)
    text = const.MSG_CHOOSE_TO_EDIT
    if not state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)
    context.user_data[states.START_OVER] = True
    return states.VOLUNTEER_FEATURE


async def ask_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод нового значения, при редактировании данных."""
    context.user_data[states.CURRENT_FEATURE] = update.callback_query.data
    text = const.MSG_ENTER_NEW_VALUE
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return states.TYPING_VOLUNTEER


async def save_volunteer_input(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения, при редактировании данных."""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.START_OVER] = True
    return await select_volunteer_field(update, context)


async def end_editing(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[states.START_OVER] = True
    await show_volunteer(update, context)
    return states.END


async def end_sending(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение в главное меню после отправки письма."""
    context.user_data[states.START_OVER] = True
    await start(update, context)
    return states.STOPPING


async def send_email(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка письма куратору."""
    user_data = context.user_data
    data = user_data.get(states.FEATURES)
    name = data.get(states.NAME, "-")
    birthday = data.get(states.BIRTHDAY, "-")
    city = data.get(states.CITY, "-")
    phone = data.get(states.PHONE, "-")
    email = data.get(states.EMAIL, "-")
    message = data.get(states.MESSAGE, "-")
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
        text=const.BTN_BACK, callback_data=str(states.SENT)
    )
    keyboard = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=keyboard
    )
    return states.VOLUNTEER_SENT
