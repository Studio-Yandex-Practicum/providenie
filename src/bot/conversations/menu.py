from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод главного меню."""
    text = "<Тут будет актуальная новость из жизни фонда.>"
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_TO_PARENTS_CHAT,
                callback_data=key.CHATS,
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_FUND, callback_data=key.REQUEST
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_VOLUNTEER,
                callback_data=key.ADD_VOLUNTEER,
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_TELL_ABOUT_FUND,
                callback_data=key.TALK,
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_DONATION, callback_data=key.DONATION
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_OUR_EVENTS, callback_data=key.EVENTS
            ),
            InlineKeyboardButton(
                text=const.BTN_TO_ASK_A_QUESTION,
                callback_data=key.ASK_QUESTION,
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_ABOUT_FUND, callback_data=key.ABOUT
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get(key.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[key.START_OVER] = False
    return state.SELECTING_ACTION


async def talk_friends(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "talk_friends"
    await update.callback_query.edit_message_text(text=text)
    return state.SELECTING_ACTION


async def give_donation(update: Update, _) -> str:
    text = const.MSG_DONATION
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_REPORTS, url=const.URL_REPORTS
            ),
            InlineKeyboardButton(
                text=const.BTN_DONATION, url=const.URL_DONATION
            ),
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
        text=text, reply_markup=keyboard
    )
    return state.SELECTING_ACTION


async def get_events(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "get_events"
    await update.callback_query.edit_message_text(text=text)
    return state.SELECTING_ACTION


async def request(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "request"
    await update.callback_query.edit_message_text(text=text)
    return state.SELECTING_ACTION


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.callback_query.answer()
    text = const.MSG_ABOUT
    button = [
        [
            InlineKeyboardButton(
                text=const.BTN_BACK,
                callback_data=str(key.END),
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(button)
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )
    context.user_data[key.START_OVER] = True
    return state.ENDING


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение работы по команде /stop."""
    context.user_data[key.START_OVER] = False
    await update.message.reply_text(const.MSG_GOODBYE)
    return key.END


async def stop_nested(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    context.user_data[key.START_OVER] = False
    await update.message.reply_text(const.MSG_GOODBYE)
    return state.STOPPING


async def end(update: Update, _) -> int:
    """Завершение разговора."""
    await update.callback_query.answer()
    return key.END


async def end_second_level(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Завершение вложенного разговора."""
    context.user_data[key.START_OVER] = True
    await start(update, context)
    return key.END


async def end_sending(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращение в главное меню после отправки данных."""
    context.user_data[key.START_OVER] = True
    await start(update, context)
    return state.STOPPING
