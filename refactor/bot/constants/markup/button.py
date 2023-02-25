from telegram import InlineKeyboardButton as Button

from bot.constants import callback
from bot.constants.info import text
from bot.constants.info.about import ABOUT_MENU, SHARE_MENU, DONATION_MENU
from bot.constants.info.form_info import FORM_INFO


'''BACK'''
main_menu = Button(
    'Назад', callback_data=callback.BACK,
)
share_menu = Button(
    'Назад', callback_data=callback.MENU_SHARE
)
donation_menu = about = Button(
    'Назад', callback_data=callback.MENU_DONATION
)
about_menu = about = Button(
    'Назад', callback_data=callback.MENU_ABOUT
)


'''MAIN MENU'''
share = Button(
    'Рассказать о Фонде своим друзьям', callback_data=callback.MENU_SHARE
)
donation = Button(
    'Отчёты и пожертвование', callback_data=callback.MENU_DONATION
)
about = Button(
    'О фонде', callback_data=callback.MENU_ABOUT
)


'''FORM'''
form_menu = Button(
    'Назад', callback_data=callback.FORM_MENU,
)

ask_input = Button(
    'Начать заполнение анкеты',
    callback_data=callback.COLLECT_DATA
)
edit_menu = Button(
    'Изменить данные', callback_data=callback.EDIT_MENU,
)
show_data = Button(
    'Назад', callback_data=callback.SHOW_DATA,
)
send_data = Button(
    'Подтвердить данные и отправить',
    callback_data=callback.SEND_DATA
)
