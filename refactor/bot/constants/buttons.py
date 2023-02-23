from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import callbacks
from bot.constants.info.forms_info import forms

main_menu_button = InlineKeyboardButton(
    'Назад', callback_data=callbacks.BACK,
)
form_menu_button = InlineKeyboardButton(
    'Назад', callback_data=callbacks.FORM_MENU,
)
show_info_button = InlineKeyboardButton(
    'Назад', callback_data=callbacks.SHOW_INFO,
)
start_data_collection_button = InlineKeyboardButton(
    'Начать заполнение анкеты',
    callback_data=callbacks.START_DATA_COLLECTION
)
forms_buttons = [
    [
        InlineKeyboardButton(
            form_info.get("button_text"), callback_data=form_name
        )
    ] for form_name, form_info in forms.items()
]

conformation_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        'Подтвердить данные и отправить',
        callback_data=callbacks.SEND_USER_INFO
    )],
    [InlineKeyboardButton(
        'Изменить данные', callback_data=callbacks.INFO_CHANGE,
    ), main_menu_button],
])