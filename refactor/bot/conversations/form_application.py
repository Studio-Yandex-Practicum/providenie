from datetime import date

from pydantic.error_wrappers import ValidationError
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import key, state, button
from bot.constants.info.question import ALL_QUESTIONS
from bot.constants.info.text import (DATE_TEMPLATE, INPUT_ERROR_TEMPLATE,
                                     SELECT_EDIT, SHOW_DATA_TEMPLATE)
from bot.utils import send_message


async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data[key.FORM] = {
        key.DATA: user_data[key.MENU][key.MODEL](),
        key.FIELD_INDEX: 0,
        key.FIELD_EDIT: False,
    }

    return await ask_input(update, context)


async def ask_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = user_data[key.MENU][key.FIELDS]

    if callback and callback.data.startswith(key.ASK):
        form[key.FIELD_EDIT] = callback.data.replace(f'{key.ASK}_', '').lower()

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]

    question = ALL_QUESTIONS[field.upper()]
    await send_message(update, question[key.TEXT])

    return state.FORM_INPUT


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = user_data[key.MENU][key.FIELDS]

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]

    try:
        setattr(form[key.DATA], field, update.message.text)
    except ValidationError:
        question_hint = ALL_QUESTIONS[field.upper()][key.HINT]
        error_message = INPUT_ERROR_TEMPLATE.format(hint=question_hint)
        await send_message(update, error_message)
        return await ask_input(update, context)

    if (form[key.FIELD_INDEX] + 1) >= len(fields):
        return await show_data(update, context)

    form[key.FIELD_INDEX] = form[key.FIELD_INDEX] + 1

    return await ask_input(update, context)


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    info = user_data[key.MENU]
    form = user_data[key.FORM]

    message = SHOW_DATA_TEMPLATE.format(title='Анкета', value=info[key.BUTTON_TEXT])
    if menu_option := user_data.get(key.OPTION):
        message += SHOW_DATA_TEMPLATE.format(title='Выбор', value=menu_option[key.BUTTON_TEXT])
    message += SHOW_DATA_TEMPLATE.format(title='Дата заявки', value=date.today().strftime(DATE_TEMPLATE))
    for name, value in form[key.DATA]:
        question = ALL_QUESTIONS[name.upper()]
        message += SHOW_DATA_TEMPLATE.format(title=question[key.TITLE], value=value)

    keyboard = Keyboard([
        [button.SEND_DATA],
        [button.EDIT_MENU, button.MAIN_MENU],
    ])
    await send_message(update, message, keyboard=keyboard)

    return state.FORM_SUBMISSION


async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    fields = user_data[key.MENU][key.FIELDS]

    edit_button = []
    for field in fields:
        question = ALL_QUESTIONS[field.upper()]
        callback = f'{key.ASK}_{field.upper()}'
        edit_button.append([Button(text=question[key.TITLE], callback_data=callback)])
    edit_button.append([button.SHOW_DATA])

    await send_message(update, SELECT_EDIT, keyboard=Keyboard(edit_button))

    return state.FORM_INPUT


async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
