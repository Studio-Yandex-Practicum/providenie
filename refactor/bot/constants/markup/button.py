from telegram import InlineKeyboardButton as Button

from bot.constants import callback


'''BACK'''
main_menu = Button(
    'Назад', callback_data=callback.BACK,
)
menu_back = Button(
    'Назад', callback_data=callback.MENU_BACK
)


'''FORM'''
start_form = Button(
    'Начать заполнение анкеты',
    callback_data=callback.START_FORM
)
send_data = Button(
    'Подтвердить и отправить',
    callback_data=callback.SEND_DATA
)
edit_menu = Button(
    'Редактировать', callback_data=callback.EDIT_MENU,
)
show_data = Button(
    'Назад', callback_data=callback.SHOW_DATA,
)
