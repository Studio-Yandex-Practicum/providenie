from telegram import BotCommand
from telegram import InlineKeyboardButton as Button

from bot.constants import callback
from bot.constants.info import text
from bot.core.settings import settings

# BACK
MAIN_MENU = Button(text.MAIN_BACK, callback_data=callback.BACK)
MENU_BACK = Button(text.BACK, callback_data=callback.MENU_BACK)


# FORM
START_FORM = Button(text.START_FORM, callback_data=callback.START_FORM)
SEND_DATA = Button(text.SEND_FORM, callback_data=callback.SEND_DATA)
EDIT_MENU = Button(text.EDIT_FORM, callback_data=callback.EDIT_MENU)
SHOW_DATA = Button(text.BACK, callback_data=callback.SHOW_DATA)

# COMMANDS
START_CMD = BotCommand('/start', text.START_CMD)
STOP_CMD = BotCommand('/stop', text.STOP_CMD)
MENU_CMD = BotCommand('/menu', text.MENU_CMD)
CANCEL_CMD = BotCommand('/cancel', text.CANCEL_CMD)

# ADMIN
ADMIN_SETTING_BTN = Button(text.ADMIN_SETTING, url=settings.admin_site_url)
ADMMIN_MAIN_MENU_BTN = Button(
    text.ADMIN_MAIN_MENU_BACK, callback_data=callback.ADMIN_BACK
)
