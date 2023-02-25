from telegram import InlineKeyboardMarkup as Keyboard

from bot.constants.markup import button


'''FORM'''
confirmation = Keyboard([
    [button.send_data],
    [button.edit_menu, button.main_menu],
])
