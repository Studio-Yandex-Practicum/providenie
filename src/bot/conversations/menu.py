from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод главного меню."""
    text = const.TXT_MEIN_MENU
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
                callback_data=key.TELL_ABOUT_FUND,
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


async def tell_friends_about_fund(update: Update, _) -> str:
    """Функция, отображающая меню со ссылками на страницы фонда."""
    text = "Выберите интересующую вас соцсеть/страницу"
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_WEBSITE, callback_data=str(key.WEBSITE)
            )
        ],
        [InlineKeyboardButton(text=const.BTN_VK, callback_data=str(key.VK))],
        [
            InlineKeyboardButton(
                text=const.BTN_INSTAGRAM, callback_data=str(key.INSTAGRAM)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_FACEBOOK, callback_data=str(key.FACEBOOK)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TG_CHANNEL, callback_data=str(key.TG_CHANNEL)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_TG_BOT, callback_data=str(key.TG_BOT)
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
        text=text, reply_markup=keyboard
    )
    return state.SOCIAL_LINKS


async def social_link(update: Update, _) -> str:
    """Функция, отображающая ссылку выбранной соцсети."""
    social_link_dict = {
        key.WEBSITE: const.MSG_WEBSITE,
        key.VK: const.MSG_VK,
        key.INSTAGRAM: const.MSG_INSTAGRAM,
        key.FACEBOOK: const.MSG_FACEBOOK,
        key.TG_CHANNEL: const.MSG_TG_CHANNEL,
        key.TG_BOT: const.MSG_TG_BOT,
    }

    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_MENU, callback_data=str(key.END)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.TELL_ABOUT_FUND)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query
    text = social_link_dict[query.data]

    await query.answer()
    await query.edit_message_text(text=text, reply_markup=keyboard)
    return state.SOCIAL_LINKS


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
