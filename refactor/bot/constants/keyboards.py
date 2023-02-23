from bot.constants import buttons
from telegram import InlineKeyboardMarkup as Keyboard

'''MAIN MENU'''
main_menu = Keyboard([
    *buttons.forms,
    [buttons.share_info],
    [buttons.donation_link, buttons.about],
])
share_menu = Keyboard([*buttons.share_links, [buttons.main_menu]])
about_menu = Keyboard([*buttons.about_options, [buttons.main_menu]])

'''FORM'''
confirmation = Keyboard([
    [buttons.info_send],
    [buttons.info_change, buttons.main_menu],
])