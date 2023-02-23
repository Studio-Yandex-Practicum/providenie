from datetime import date

from pydantic.error_wrappers import ValidationError
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import callback, key, state
from bot.constants.info.form_info import FORM_INFO
from bot.constants.info.question import ALL_QUESTIONS
from bot.constants.markup import button, keyboard
from bot.utils import send_message


SHOW_DATA_TEMPLATE = '<b><u>{title}</u></b>:\n\t\t{value}\n\n'
INPUT_ERROR_TEMPLATE = '<b>Некорректный ввод</b>: \n{message}'
DATE_FORMAT = '%d.%m.%Y'


async def form_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data
    form_name = query.data

    if form_name == callback.FORM_MENU:
        info = user_data[key.FORM][key.INFO]
    else:
        info = FORM_INFO[form_name]
        user_data[key.FORM] = {key.INFO: info}

    if not (menu := info.get('menu')):
        return await confirm_selection(update, context)

    menu_button = [
        [Button(text=option.get('name'), callback_data=callback)]
        for callback, option in menu.items()
    ]
    menu_keyboard = Keyboard([*menu_button, [button.main_menu]])

    await send_message(update, info['desc'], keyboard=menu_keyboard)

    return state.FORM_CHOOSING


async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    form = context.user_data[key.FORM]
    info = form[key.INFO]

    form[key.APPLICATION] = info['model']()
    form[key.QUESTION_INDEX] = 0
    form[key.EDIT_FIELD] = False

    if menu := info.get('menu'):
        option = menu[query.data]
        form[key.SELECTED_OPTION] = option['name']
        confirm_text = option['desc']
        back_button = button.form_menu
    else:
        confirm_text = info['desc']
        back_button = button.main_menu

    keyboard = Keyboard([[button.info_collect, back_button]])

    await send_message(update, confirm_text, keyboard=keyboard)

    return state.FORM_CONFIRMATION


async def ask_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]
    fields = form[key.INFO]['fields']
    query = update.callback_query

    if query and query.data.startswith(key.INPUT):
        field = query.data.replace(f'{key.INPUT}_', '')
        question = ALL_QUESTIONS[field]
        form[key.EDIT_FIELD] = field.lower()
    elif question_name := form.get(key.EDIT_FIELD):
        question = ALL_QUESTIONS[question_name.upper()]
    else:
        field = fields[form[key.QUESTION_INDEX]]
        question = ALL_QUESTIONS[field.upper()]

    await send_message(update, question['text'] + ':')

    return state.FORM_TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]
    fields = form[key.INFO]['fields']
    text = update.message.text

    field = form.get(key.EDIT_FIELD)
    if not field:
        field = fields[form[key.QUESTION_INDEX]]

    try:
        setattr(form[key.APPLICATION], field, text)
    except ValidationError as errors:
        errors_message = '\n'.join(error['msg'] for error in errors.errors())
        await send_message(update, INPUT_ERROR_TEMPLATE.format(message=errors_message))
        return await ask_input(update, context)

    if form.get(key.EDIT_FIELD) or (form[key.QUESTION_INDEX] + 1) >= len(fields):
        return await show_data(update, context)

    form[key.QUESTION_INDEX] = form[key.QUESTION_INDEX] + 1

    return await ask_input(update, context)


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]

    message = SHOW_DATA_TEMPLATE.format(title='Анкета', value=form[key.INFO]['name'])
    if menu_option := form.get(key.SELECTED_OPTION):
        message += SHOW_DATA_TEMPLATE.format(title='Выбор', value=menu_option)
    message += SHOW_DATA_TEMPLATE.format(title='Дата заявки', value=date.today().strftime(DATE_FORMAT))

    for name, value in form[key.APPLICATION]:
        question = ALL_QUESTIONS[name.upper()]
        message += SHOW_DATA_TEMPLATE.format(title=question['name'], value=value)

    await send_message(update, message, keyboard=keyboard.confirmation)

    return state.FORM_CONFIRMATION


async def edit_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data[key.FORM]
    edit_button = []
    for field in form[key.INFO]['fields']:
        question = ALL_QUESTIONS[field.upper()]
        callback = f'{key.INPUT}_{field.upper()}'
        edit_button.append([Button(text=question['name'], callback_data=callback)])
    edit_button.append([button.info_show])

    await send_message(update, 'Что изменить: ', keyboard=Keyboard(edit_button))

    return state.FORM_CHOOSING
