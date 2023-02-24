from telegram import InlineKeyboardMarkup as Keyboard

from bot.constants.markup import button


'''MAIN MENU'''
main_menu = Keyboard([
    *button.forms,
    [button.share_info],
    [button.donation_link, button.about],
])
share_menu = Keyboard([*button.share_links, [button.main_menu]])
about_menu = Keyboard([*button.about_options, [button.main_menu]])

'''FORM'''
confirmation = Keyboard([
    [button.data_send],
    [button.data_edit, button.main_menu],
])