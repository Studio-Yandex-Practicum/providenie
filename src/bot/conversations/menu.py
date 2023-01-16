from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import states


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод главного меню."""
    text = "<Тут будет актуальная новость из жизни фонда.>"
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_TO_PARENTS_CHAT,
                callback_data=str(states.CHATS),
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_FUND, callback_data=str(states.REQUEST)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_VOLUNTEER,
                callback_data=str(states.ADD_VOLUNTEER),
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_TELL_ABOUT_FUND,
                callback_data=str(states.TALK),
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_DONATION, callback_data=str(states.DONATION)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_OUR_EVENTS, callback_data=str(states.EVENTS)
            ),
            InlineKeyboardButton(
                text=const.BTN_TO_ASK_A_QUESTION,
                callback_data=str(states.QUESTION),
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TO_ABOUT_FUND, callback_data=str(states.ABOUT)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get(states.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[states.START_OVER] = False
    return states.SELECTING_ACTION


async def talk_friends(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "talk_friends"
    await update.callback_query.edit_message_text(text=text)
    return states.SELECTING_ACTION


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
                text=const.BTN_BACK, callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )
    return states.SELECTING_ACTION


async def get_events(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "get_events"
    await update.callback_query.edit_message_text(text=text)
    return states.SELECTING_ACTION


async def ask_question(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "ask_question"
    await update.callback_query.edit_message_text(text=text)
    return states.SELECTING_ACTION


async def request(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "request"
    await update.callback_query.edit_message_text(text=text)
    return states.SELECTING_ACTION


async def about(update: Update, _) -> str:
    await update.callback_query.answer()
    text = "Информация о фонде"
    button = [
        [
            InlineKeyboardButton(
                text="Возврат в главное меню",
                callback_data=str(states.START_OVER),
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(button)
    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=keyboard
    )
    return states.SELECTING_ACTION


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение работы по команде /stop."""
    context.user_data[states.START_OVER] = False
    await update.message.reply_text(const.MSG_GOODBYE)
    return states.END


async def stop_nested(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    context.user_data[states.START_OVER] = False
    await update.message.reply_text(const.MSG_GOODBYE)
    return states.STOPPING


async def end(update: Update, _) -> int:
    """Завершение разговора."""
    await update.callback_query.answer()
    return states.END


async def end_second_level(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Завершение вложенного разговора."""
    context.user_data[states.START_OVER] = True
    await start(update, context)
    return states.END


async def select_chat(update: Update, _) -> str:
    """Эту функцию надо будет перенести.
    В файл conversations/parents_chat.py.
    """
    await update.callback_query.answer()
    text = "select_chat"
    await update.callback_query.edit_message_text(text=text)
    return states.SELECTING_ACTION
