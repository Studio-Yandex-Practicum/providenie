from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import constants as const
from bot import keys as key
from bot import states as state
from bot.flags.flag import Flags


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод главного меню."""
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
                text=const.BTN_TO_ABOUT_FUND, callback_data=key.ABOUT_FUND
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if not context.user_data.get(key.FLAGS):
        context.user_data[key.FLAGS] = Flags()

    if context.user_data.get(key.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=const.MSG_START, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text=const.MSG_START, reply_markup=keyboard
        )

    context.user_data[key.START_OVER] = False
    return state.SELECTING_ACTION


async def tell_friends_about_fund(update: Update, _) -> str:
    """Функция, отображающая меню со ссылками на страницы фонда."""
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
        text=const.MSG_TELL_ABOUT, reply_markup=keyboard
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

    await query.answer()
    await query.edit_message_text(
        text=social_link_dict[query.data], reply_markup=keyboard
    )
    return state.SOCIAL_LINKS


async def give_donation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Функция, отображающая ссылки на меню отчетов о пожертвованиях"""
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
                text=const.BTN_MENU, callback_data=str(key.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_DONATION, reply_markup=keyboard
    )
    context.user_data[key.START_OVER] = True
    return state.ENDING


async def get_events(update: Update, _) -> str:
    buttons =[
        [
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=const.MSG_EVENTS, reply_markup=keyboard)
    return state.STOPPING


async def about(update: Update, _) -> str:
    """Функция, отображающая информации о фонде"""
    social_dict = {
        key.WHO_ARE_WE: const.URL_WHO_ARE_WE,
        key.PROBLEM_SOLVING: const.URL_PROBLEM_SOLVING,
        key.WHAT_PROBLEM_SOLVING: const.URL_WHAT_PROBLEM_SOLVING,
        key.LIFE_CHANGE: const.URL_LIFE_CHANGE,
        key.WHAT_IS_DONE: const.URL_WHAT_IS_DONE,
        key.DONATION_NEED: const.URL_DONATION_NEED,
        key.ABOUT_SUCCESS: key.ABOUT_SUCCESS,
    }
    buttons = [
        [
            InlineKeyboardButton(
                text=const.BTN_MENU, callback_data=str(key.END)
            )
        ],
        [
            InlineKeyboardButton(
                text=const.BTN_BACK, callback_data=str(key.ABOUT_FUND)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query
    text = social_dict[query.data]

    await query.answer()
    await query.edit_message_text(text=text, reply_markup=keyboard)
    return state.ABOUT_INFO


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
