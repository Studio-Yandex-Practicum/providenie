from telegram import InlineKeyboardButton, InlineKeyboardMarkup

start_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Начать заполнение анкеты',
            callback_data=callbacks.START_DATA_COLLECTION
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK,
        )],
    ])
