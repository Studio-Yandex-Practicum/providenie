from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states
from bot.conversations.menu import start
from core.email import bot_send_email_to_curator


async def add_volunteer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Путь вступления в ряды волонтёров."""
    user_data = context.user_data
    user_data[states.START_OVER] = False
    text = "Далее необходимо предоставить информацию для куратора"
    buttons = [
        [
            InlineKeyboardButton(
                text="Начать", callback_data=str(states.VOLUNTEER)
            ),
            InlineKeyboardButton(text="Назад", callback_data=str(states.END)),
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
    text = "Фамилия, Имя, Отчество?"
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
    text = "Дата рождения?"
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
    text = "Город проживания?"
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
    text = "Номер телефона?"
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
    text = "Email?"
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
    text = (
        "Вы можете предложить свой вариант помощи (необязательно). "
        "Нажмите /skip чтобы пропустить."
    )
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
    if not data:
        text = "\nДанных нет.\n"
    else:
        text = (
            f'Ф.И.О.\n {data.get(states.NAME, "-")}\n'
            f'Дата рождения\n {data.get(states.BIRTHDAY, "-")}\n'
            f'Город\n {data.get(states.CITY, "-")}\n'
            f'Телефон\n {data.get(states.PHONE, "-")}\n'
            f'Email\n {data.get(states.EMAIL, "-")}\n'
            f'Сообщение\n {data.get(states.MESSAGE, "-")}\n'
        )
    buttons = [
        [
            InlineKeyboardButton(
                text="Редактировать", callback_data=str(states.EDIT_VOLUNTEER)
            ),
            InlineKeyboardButton(
                text="Отправить", callback_data=str(states.SEND_VOLUNTEER)
            ),
            InlineKeyboardButton(text="Назад", callback_data=str(states.END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(states.START_OVER)
    if state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)
    user_data[states.START_OVER] = False
    return states.SHOWING_VOLUNTEER


async def select_volunteer_field(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод меню редактирования введённых ранее данных."""
    buttons = [
        [
            InlineKeyboardButton(
                text="Ф.И.О.", callback_data=str(states.NAME)
            ),
            InlineKeyboardButton(
                text="Дата рождения", callback_data=str(states.BIRTHDAY)
            ),
            InlineKeyboardButton(text="Город", callback_data=str(states.CITY)),
            InlineKeyboardButton(
                text="Телефон", callback_data=str(states.PHONE)
            ),
            InlineKeyboardButton(
                text="Email", callback_data=str(states.EMAIL)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Ваш вариант помощи", callback_data=str(states.MESSAGE)
            ),
            InlineKeyboardButton(text="Готово", callback_data=str(states.END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(states.START_OVER)
    text = "Выберите для редактирования:"
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
    text = "Введите новое значение:"
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
    subject = "Новый волонтёр"
    html = f"""
        <html>
            <body>
                <h1>{subject}</h1>
                <p>
                    <b>ФИО:</b> {name}<br/>
                    <b>Дата рождения:</b> {birthday}<br/>
                    <b>Город проживания:</b> {city}<br/>
                    <b>Телефон:</b> {phone}<br/>
                    <b>Почта:</b> {email}<br/>
                    <b>Вариант помощи:</b> {message}
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
    button = InlineKeyboardButton(text="Назад", callback_data=str(states.SENT))
    keyboard = InlineKeyboardMarkup.from_button(button)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=return_text, reply_markup=keyboard
    )
    return states.VOLUNTEER_SENT
