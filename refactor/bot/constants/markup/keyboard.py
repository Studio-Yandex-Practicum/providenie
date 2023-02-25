from telegram import InlineKeyboardMarkup as Keyboard

from bot.constants.markup import button


'''MAIN MENU'''
main_menu = Keyboard([
    *button.forms,
    [button.share_info],
    [button.event, button.about],
])
share_menu = Keyboard([*button.share_links, [button.main_menu]])
about_menu = Keyboard([*button.about_options, [button.main_menu]])
donation_menu = Keyboard([button.donation_links])

'''FORM'''
confirmation = Keyboard([
    [button.send_data],
    [button.edit_menu, button.main_menu],
])
