from datetime import date

from pydantic.error_wrappers import ValidationError
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import callback, key, state
from bot.constants.info.form_info import FORM_INFO
from bot.constants.info.text import (DATE_TEMPLATE,
                                     INPUT_ERROR_TEMPLATE,
                                     MSG_CHOOSE_TO_EDIT,
                                     SHOW_DATA_TEMPLATE)
from bot.constants.info.question import ALL_QUESTIONS
from bot.constants.markup import button, keyboard
from bot.utils import send_message, get_menu_buttons


async def form_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data
    form_name = query.data

    if form_name == callback.FORM_MENU:
        info = user_data[key.FORM][key.INFO]
    else:
        info = FORM_INFO[form_name]
        user_data[key.FORM] = {key.INFO: info}

    if not (menu := info.get(key.MENU)):
        return await confirm_selection(update, context)

    menu_keyboard = Keyboard([*get_menu_buttons(menu), [button.main_menu]])

    await send_message(update, info[key.DESCRIPTION], keyboard=menu_keyboard)

    return state.FORM_SELECTION


async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    form = context.user_data[key.FORM]
    info = form[key.INFO]

    form[key.DATA] = info[key.MODEL]()
    form[key.FIELD_INDEX] = 0
    form[key.FIELD_EDIT] = False

    if menu := info.get(key.MENU):
        option = menu[query.data]
        form[key.SELECTED_OPTION] = option[key.BUTTON_TEXT]
        confirm_text = f"{option[key.BUTTON_TEXT]}\n"
        confirm_text += option[key.DESCRIPTION]
        back_button = button.form_menu
    else:
        confirm_text = info[key.DESCRIPTION]
        back_button = button.main_menu

    keyboard = Keyboard([[button.ask_input, back_button]])

    await send_message(update, confirm_text, keyboard=keyboard)

    return state.FORM_SUBMISSION


async def ask_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]
    fields = form[key.INFO][key.FIELDS]
    query = update.callback_query

    if query and query.data.startswith(key.ASK):
        field = query.data.replace(f'{key.ASK}_', '')
        question = ALL_QUESTIONS[field]
        form[key.FIELD_EDIT] = field.lower()
    elif field := form.get(key.FIELD_EDIT):
        question = ALL_QUESTIONS[field.upper()]
    else:
        field = fields[form[key.FIELD_INDEX]]
        question = ALL_QUESTIONS[field.upper()]

    await send_message(update, question[key.TEXT] + ':')

    return state.FORM_INPUT


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]
    fields = form[key.INFO][key.FIELDS]
    input_value = update.message.text

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]

    try:
        setattr(form[key.DATA], field, input_value)
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
    form = context.user_data[key.FORM]

    message = SHOW_DATA_TEMPLATE.format(title='Анкета', value=form[key.INFO][key.BUTTON_TEXT])
    if menu_option := form.get(key.SELECTED_OPTION):
        message += SHOW_DATA_TEMPLATE.format(title='Выбор', value=menu_option)
    message += SHOW_DATA_TEMPLATE.format(title='Дата заявки', value=date.today().strftime(DATE_TEMPLATE))

    for name, value in form[key.DATA]:
        question = ALL_QUESTIONS[name.upper()]
        message += SHOW_DATA_TEMPLATE.format(title=question[key.TITLE], value=value)

    await send_message(update, message, keyboard=keyboard.confirmation)

    return state.FORM_SUBMISSION


async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]
    edit_button = []
    for field in form[key.INFO][key.FIELDS]:
        question = ALL_QUESTIONS[field.upper()]
        callback = f'{key.ASK}_{field.upper()}'
        edit_button.append([Button(text=question[key.TITLE], callback_data=callback)])
    edit_button.append([button.show_data])

    await send_message(update, MSG_CHOOSE_TO_EDIT, keyboard=Keyboard(edit_button))

    return state.FORM_INPUT


async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
