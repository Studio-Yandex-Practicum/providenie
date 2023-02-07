from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from bot import constants as const
from bot import keys as key
from bot import states as state


async def select_about_found(update: Update, _) -> str:
    """Вывод меню информации о фонде."""
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_WHO_ARE_WE, callback_data=key.WHO_ARE_WE
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_PROBLEM_SOLVING,
                callback_data=key.PROBLEM_SOLVING,
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_WHAT_PROBLEM_SOLVING,
                callback_data=key.WHAT_PROBLEM_SOLVING,
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_LIFE_CHANGE, callback_data=key.LIFE_CHANGE
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_WHAT_IS_DONE, callback_data=key.WHAT_IS_DONE
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_DONATION_NEED, callback_data=key.DONATION_NEED
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_SUCCESS, callback_data=key.ABOUT_SUCCESS
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_ABOUT, reply_markup=keyboard
    )
    return state.ABOUT_INFO


async def select_success_found(update: Update, _) -> str:
    """Вывод меню ссылок на видео успехаов фонда."""
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_SUCCESS_VIDEO1, url=const.URL_VIDEO_1
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_SUCCESS_VIDEO2, url=const.URL_VIDEO_2
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_SUCCESS_VIDEO3, url=const.URL_VIDEO_3
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_SUCCESS_VIDEO4, url=const.URL_VIDEO_4
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_SUCCESS_VIDEO5, url=const.URL_VIDEO_5
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_MENU, callback_data=str(key.END)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=key.ABOUT_FUND
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_ABOUT_SUCCESS, reply_markup=keyboard
    )
    return state.ABOUT_INFO
