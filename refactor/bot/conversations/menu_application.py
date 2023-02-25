from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import callback, key, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.constants.markup import button
from bot.utils import get_menu_buttons, send_message


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data
    menu_name = query.data

    if menu_name == callback.MENU_BACK:
        menu = user_data[key.MENU]
    else:
        menu = ALL_MENU[menu_name]
        user_data[key.MENU] = menu

    if not (options := menu.get(key.OPTIONS)):
        return await show_option(update, context)

    menu_keyboard = Keyboard([*get_menu_buttons(options), [button.main_menu]])

    await send_message(update, menu[key.BUTTON_TEXT], keyboard=menu_keyboard)

    return state.MAIN_MENU


async def show_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data
    menu = user_data[key.MENU]

    if options := menu.get(key.OPTIONS):
        option = options[query.data]
        user_data[key.OPTION] = option
        message = text.SHOW_DATA_TEMPLATE.format(title=option[key.BUTTON_TEXT], value=option[key.DESCRIPTION])
        back_button = button.menu_back
    else:
        message = menu[key.DESCRIPTION]
        back_button = button.main_menu

    buttons = [back_button]
    if menu.get(key.MODEL):
        buttons.insert(0, button.start_form)
    if options and (url := option.get(key.LINK)):
        buttons.insert(0, Button(text.OPTION_URL, url=url))

    await send_message(update, message, keyboard=Keyboard([buttons]))

    return state.MAIN_MENU
