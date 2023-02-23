from datetime import date
from typing import Optional

from pydantic.error_wrappers import ValidationError
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import states, callbacks
from bot.constants import buttons
from bot.constants import keys
from bot.constants.info.forms_info import forms
from bot.constants.info.question import questionnaire


MESSAGE_MARKDOWN = 'HTML'
SHOW_DATA_TEMPLATE = '<b><u>{title}</u></b>:\n\t\t{value}\n\n'
INPUT_ERROR_TEMPLATE = '<b>Некорректный ввод</b>: \n{message}'
DATE_FORMAT = '%d.%m.%Y'


async def send_message(update: Update, message: str, keyboard: Optional[Keyboard] = None):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.edit_text(message, reply_markup=keyboard, parse_mode=MESSAGE_MARKDOWN)
    else:
        await update.message.reply_text(message, reply_markup=keyboard, parse_mode=MESSAGE_MARKDOWN)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data
    form_name = query.data

    if form_name == callbacks.FORM_MENU:
        form_info = user_data[keys.FORM][keys.INFO]
    else:
        form_info = forms[form_name]
        user_data[keys.FORM] = {keys.INFO: form_info}

    if not (menu := form_info.get('menu')):
        return await confirm_selection(update, context)

    menu_buttons = [
        [Button(text=option.get('name'), callback_data=callback)]
        for callback, option in menu.items()
    ]
    menu_keyboard = Keyboard([*menu_buttons, [buttons.main_menu_button]])

    await send_message(update, form_info['desc'], keyboard=menu_keyboard)

    return states.CHOOSING


async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    form = context.user_data[keys.FORM]
    form_info = form[keys.INFO]

    form[keys.APPLICATION] = form_info['model']()
    form[keys.QUESTION_INDEX] = 0
    form[keys.EDIT_FIELD] = False

    if menu := form_info.get('menu'):
        option = menu[query.data]
        form[keys.SELECTED_OPTION] = option['name']
        confirm_text = option['desc']
        back_button = buttons.form_menu_button
    else:
        confirm_text = form_info['desc']
        back_button = buttons.main_menu_button

    keyboard = Keyboard([[buttons.start_data_collection_button, back_button]])

    await send_message(update, confirm_text, keyboard=keyboard)

    return states.CONFIRMATION


async def ask_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[keys.FORM]
    fields = form[keys.INFO]['fields']
    query = update.callback_query

    if query and query.data.startswith(keys.INPUT):
        field = query.data.replace(f'{keys.INPUT}_', '')
        question = questionnaire[field]
        form[keys.EDIT_FIELD] = field.lower()
    elif question_name := form.get(keys.EDIT_FIELD):
        question = questionnaire[question_name.upper()]
    else:
        field = fields[form[keys.QUESTION_INDEX]]
        question = questionnaire[field.upper()]

    await send_message(update, question['text'] + ':')

    return states.TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[keys.FORM]
    fields = form[keys.INFO]['fields']
    text = update.message.text

    field = form.get(keys.EDIT_FIELD)
    if not field:
        field = fields[form[keys.QUESTION_INDEX]]

    try:
        setattr(form[keys.APPLICATION], field, text)
    except ValidationError as errors:
        errors_message = '\n'.join(error['msg'] for error in errors.errors())
        await send_message(update, INPUT_ERROR_TEMPLATE.format(message=errors_message))
        return await ask_input(update, context)

    if form.get(keys.EDIT_FIELD) or (form[keys.QUESTION_INDEX] + 1) >= len(fields):
        return await show_data(update, context)

    form[keys.QUESTION_INDEX] = form[keys.QUESTION_INDEX] + 1

    return await ask_input(update, context)


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[keys.FORM]

    message = SHOW_DATA_TEMPLATE.format(title='Анкета', value=form[keys.INFO]['name'])
    if menu_option := form.get(keys.SELECTED_OPTION):
        message += SHOW_DATA_TEMPLATE.format(title='Выбор', value=menu_option)
    message += SHOW_DATA_TEMPLATE.format(title='Дата заявки', value=date.today().strftime(DATE_FORMAT))

    for name, value in form[keys.APPLICATION]:
        question = questionnaire[name.upper()]
        message += SHOW_DATA_TEMPLATE.format(title=question['name'], value=value)

    await send_message(update, message, keyboard=buttons.conformation_keyboard)

    return states.CONFIRMATION


async def edit_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[keys.FORM]
    edit_buttons = []
    for field in form[keys.INFO]['fields']:
        question = questionnaire[field.upper()]
        callback = f'{keys.INPUT}_{field.upper()}'
        edit_buttons.append([Button(text=question['name'], callback_data=callback)])
    edit_buttons.append([buttons.show_info_button])

    await send_message(update, 'Что изменить: ', keyboard=Keyboard(edit_buttons))

    return states.CHOOSING
