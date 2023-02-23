from telegram import InlineKeyboardButton as Button

from bot.constants import callbacks
from bot.constants.info.forms_info import forms_info
from bot.constants.info.about import ABOUT_OPTIONS, SHARE_LINKS

'''BACK'''
main_menu = Button(
    'Назад', callback_data=callbacks.BACK,
)
share_menu = Button(
    'Назад', callback_data=callbacks.SHARE_INFO
)
about_menu = about = Button(
    'Назад', callback_data=callbacks.MENU_ABOUT
)


'''MAIN MENU'''
forms = [
    [
        Button(info.get("button_text"), callback_data=callback)
    ] for callback, info in forms_info.items()
]
share_info = Button(
    'Рассказать о фонде своим друзьям', callback_data=callbacks.SHARE_INFO
)
share_links = [
    [
        Button(link.get("name"), callback_data=callback)
    ] for callback, link in SHARE_LINKS.items()
]

donation_link = Button(  # TODO Перенеси в константы
    'Сделать пожертвование', url="https://fond-providenie.ru/help-chidren/sdelat-pozhertovanie/sdelat-pozhertvovanie-s-bankovskoj-karty/"
)

about = Button(
    'Узнать о фонде', callback_data=callbacks.MENU_ABOUT
)
about_options = [
    [
        Button(about.get("name"), callback_data=calback)
    ] for calback, about in ABOUT_OPTIONS.items()
]


'''FORM'''
form_menu = Button(
    'Назад', callback_data=callbacks.FORM_MENU,
)
info_show = Button(
    'Назад', callback_data=callbacks.INFO_SHOW,
)
info_collect = Button(
    'Начать заполнение анкеты',
    callback_data=callbacks.INFO_COLLECT
)
info_send = Button(
    'Подтвердить данные и отправить',
    callback_data=callbacks.INFO_SEND
)
info_change = Button(
    'Изменить данные', callback_data=callbacks.INFO_CHANGE,
)
