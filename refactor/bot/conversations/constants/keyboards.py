from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot import callbacks

back_button = InlineKeyboardButton(
    'Назад', callback_data=callbacks.BACK,
)

form_menu_button = InlineKeyboardButton(
    'Назад', callback_data=callbacks.NESTED_MENU,
)

start_data_collection_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        'Начать заполнение анкеты',
        callback_data=callbacks.START_DATA_COLLECTION
    )],
    [form_menu_button],
])
