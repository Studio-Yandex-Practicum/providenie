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
    """Путь вступления в ряды волонтёров."""
    user_data = context.user_data
    user_data[key.START_OVER] = False
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_BEGIN, callback_data=key.VOLUNTEER
            ),
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.END)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_NEED_INFORMATION, reply_markup=keyboard
    )
    return state.ADDING_VOLUNTEER


async def ask_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем ФИО."""
    user_data = context.user_data
    user_data[key.FEATURES] = {key.LEVEL: key.VOLUNTEER}
    user_data[key.CURRENT_FEATURE] = key.NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=const.MSG_FULL_NAME)
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


async def ask_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем ФИО, спрашиваем дату рождения."""
    await save_feature(update, context, key.BIRTHDAY, const.MSG_BIRTHDAY)
    return state.ADDING_BIRTHDAY


async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сохраняем дату рождения, спрашиваем город проживания."""
    await save_feature(update, context, key.CITY, const.MSG_CITY)
    return state.ADDING_CITY


async def ask_phone_number(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем город проживания, спрашиваем номер телефона."""
    await save_feature(update, context, key.PHONE, const.MSG_PHONE)
    return state.ADDING_PHONE


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сохраняем номер телефона, спрашиваем email."""
    await save_feature(update, context, key.EMAIL, const.MSG_EMAIL)
    return state.ADDING_EMAIL


async def ask_help_option(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем email, спрашиваем вариант помощи."""
    await save_feature(
        update, context, key.MESSAGE, const.MSG_YOUR_HELP_OPTION
    )
    return state.ADDING_MESSAGE


async def save_help_option(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем вариант помощи."""
    await save_feature(update, context)
    return await display_entered_value(update, context)


async def skip_adding_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем пустой вариант помощи."""
    user_data = context.user_data
    user_data[key.FEATURES][user_data[key.CURRENT_FEATURE]] = ""
    return await display_entered_value(update, context)


async def display_entered_value(
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
                text=const.BTN_EDIT, callback_data=key.EDIT_VOLUNTEER
            ),
            InlineKeyboardButton(
                text=const.BTN_SEND, callback_data=key.SEND_VOLUNTEER
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


async def display_editing_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_FULL_NAME, callback_data=key.NAME
            ),
            InlineKeyboardButton(
                text=const.BTN_BIRTHDAY, callback_data=key.BIRTHDAY
            ),
        ],
        [
            InlineKeyboardButton(text=const.BTN_CITY, callback_data=key.CITY),
            InlineKeyboardButton(
                text=const.BTN_PHONE, callback_data=key.PHONE
            ),
            InlineKeyboardButton(
                text=const.BTN_EMAIL, callback_data=key.EMAIL
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_YOUR_HELP_OPTION,
                callback_data=key.MESSAGE,
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


async def ask_new_value(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Ввод нового значения, при редактировании данных."""
    context.user_data[key.CURRENT_FEATURE] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_ENTER_NEW_VALUE
    )
    return state.TYPING_VOLUNTEER


async def save_new_value(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохранение нового значения, при редактировании данных."""
    await save_feature(update, context)
    context.user_data[key.START_OVER] = True
    return await display_editing_menu(update, context)


async def display_all_new_entered_value(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение к просмотру данных после редактирования."""
    context.user_data[key.START_OVER] = True
    await display_entered_value(update, context)
    return key.END


async def send_email_to_curator(
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
    button = InlineKeyboardButton(text=const.BTN_BACK, callback_data=key.SENT)
    keyboard = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=keyboard
    )
    return state.VOLUNTEER_SENT
