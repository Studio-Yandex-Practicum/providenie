from telegram import BotCommandScopeChat
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import button, callback, key, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.utils import get_menu_buttons, send_message


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the selected menu or sub-menu to the user."""
    await context.bot.set_my_commands(
        [button.MENU_CMD],
        scope=BotCommandScopeChat(update.effective_chat.id),
    )
    query = update.callback_query
    user_data = context.user_data

    if not query or query.data == callback.MENU_BACK:
        menu = user_data[key.MENU]
        user_data.pop(key.OPTION, None)
    else:
        menu = ALL_MENU[query.data]
        user_data[key.MENU] = menu

    if not (options := menu.get(key.OPTIONS)):
        return await show_option(update, context)

    menu_keyboard = Keyboard([*get_menu_buttons(options), [button.MAIN_MENU]])

    await send_message(update, menu[key.DESCRIPTION], keyboard=menu_keyboard)

    return state.MAIN_MENU


async def show_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the option selected from the menu."""
    query = update.callback_query
    user_data = context.user_data
    menu = user_data[key.MENU]
    options = menu.get(key.OPTIONS)

    if query and query.data.startswith(key.OPTION):
        option = options[query.data]
        user_data[key.OPTION] = option
        title = option.get(key.NAME, option[key.BUTTON_TEXT])
        message = text.SHOW_DATA_TEMPLATE.format(
            title=title, value=option.get(key.DESCRIPTION, '')
        )
        back_button = button.MENU_BACK
    else:
        message = menu[key.DESCRIPTION]
        back_button = button.MAIN_MENU

    buttons = [back_button]
    if menu.get(key.MODEL):
        buttons.insert(0, button.START_FORM)
    if options and (url := option.get(key.LINK)):
        buttons.insert(0, Button(text.FOLLOW_LINK, url=url))

    await send_message(update, message, keyboard=Keyboard([buttons]))

    return state.MAIN_MENU
