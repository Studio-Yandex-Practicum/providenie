from telegram import InlineKeyboardButton as Button

from bot.constants import callback
from bot.constants.info.about import ABOUT_OPTIONS, SHARE_LINKS
from bot.constants.info.form_info import FORM_INFO


'''BACK'''
main_menu = Button(
    'Назад', callback_data=callback.BACK,
)
share_menu = Button(
    'Назад', callback_data=callback.SHARE_INFO
)
about_menu = about = Button(
    'Назад', callback_data=callback.MENU_ABOUT
)


'''MAIN MENU'''
forms = [
    [
        Button(info.get("button_text"), callback_data=callback)
    ] for callback, info in FORM_INFO.items()
]
share_info = Button(
    'Рассказать о фонде своим друзьям', callback_data=callback.SHARE_INFO
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
    'Узнать о фонде', callback_data=callback.MENU_ABOUT
)
about_options = [
    [
        Button(about.get("name"), callback_data=calback)
    ] for calback, about in ABOUT_OPTIONS.items()
]


'''FORM'''
form_menu = Button(
    'Назад', callback_data=callback.FORM_MENU,
)
data_show = Button(
    'Назад', callback_data=callback.DATA_SHOW,
)
data_collect = Button(
    'Начать заполнение анкеты',
    callback_data=callback.DATA_COLLECT
)
data_send = Button(
    'Подтвердить данные и отправить',
    callback_data=callback.DATA_SEND
)
data_edit = Button(
    'Изменить данные', callback_data=callback.DATA_EDIT,
)
