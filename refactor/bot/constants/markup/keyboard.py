from telegram import InlineKeyboardMarkup as Keyboard

from bot.constants.markup import button
from bot.constants.info.about import ABOUT_MENU, SHARE_MENU, DONATION_MENU
from bot.constants.info.form_info import FORM_INFO
from bot.utils import get_menu_buttons

'''MAIN MENU'''
main_menu = Keyboard([
    *get_menu_buttons(FORM_INFO),
    [button.share],
    [button.donation, button.about],
])
share_menu = Keyboard([*get_menu_buttons(SHARE_MENU), [button.main_menu]])
about_menu = Keyboard([*get_menu_buttons(ABOUT_MENU), [button.main_menu]])
donation_menu = Keyboard([*get_menu_buttons(DONATION_MENU), [button.main_menu]])

'''FORM'''
confirmation = Keyboard([
    [button.send_data],
    [button.edit_menu, button.main_menu],
])
