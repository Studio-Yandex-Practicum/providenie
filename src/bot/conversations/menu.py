from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод главного меню."""
    text = "Тут будет актуальная новость из жизни фонда."
    buttons = [
        [
            InlineKeyboardButton(
                text="Хочу попасть в родительский чат",
                callback_data=str(states.CHATS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Заявка в фонд", callback_data=str(states.REQUEST)
            )
        ],
        [
            InlineKeyboardButton(
                text="Хочу стать волонтёром",
                callback_data=str(states.ADD_VOLUNTEER),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Рассказать о Фонде своим друзьям",
                callback_data=str(states.TALK),
            )
        ],
        [
            InlineKeyboardButton(
                text="Пожертвование", callback_data=str(states.DONATION)
            )
        ],
        [
            InlineKeyboardButton(
                text="Наши события", callback_data=str(states.EVENTS)
            ),
            InlineKeyboardButton(
                text="Задать вопрос", callback_data=str(states.QUESTION)
            ),
        ],
        [
            InlineKeyboardButton(
                text="О Фонде", callback_data=str(states.ABOUT)
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
    await update.callback_query.answer()
    text = "give_donation"
    await update.callback_query.edit_message_text(text=text)
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


async def stop(update: Update, _) -> int:
    """Завершение работы по команде /stop."""
    await update.message.reply_text(
        "До свидания! Будем рады видеть Вас на нашем сайте!\n"
        "https://fond-providenie.ru\n"
        "Нажмите /start для повторного запуска"
    )
    return states.END


async def stop_nested(update: Update, _) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    await update.message.reply_text(
        "До свидания! Будем рады видеть Вас на нашем сайте!\n"
        "https://fond-providenie.ru\n"
        "Нажмите /start для повторного запуска"
    )
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
