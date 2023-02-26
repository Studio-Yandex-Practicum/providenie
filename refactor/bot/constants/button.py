from telegram import InlineKeyboardButton as Button

from bot.constants import callback
from bot.constants.info.text import BACK, EDIT_FORM, SEND_FORM, START_FORM


"""BACK"""
MAIN_MENU = Button(BACK, callback_data=callback.BACK)
MENU_BACK = Button(BACK, callback_data=callback.MENU_BACK)


"""FORM"""
START_FORM = Button(START_FORM, callback_data=callback.START_FORM)
SEND_DATA = Button(SEND_FORM, callback_data=callback.SEND_DATA)
EDIT_MENU = Button(EDIT_FORM, callback_data=callback.EDIT_MENU)
SHOW_DATA = Button(BACK, callback_data=callback.SHOW_DATA)
