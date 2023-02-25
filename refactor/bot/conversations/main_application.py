from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update, BotCommand
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
from bot.constants.info import text
from bot.constants.info.about import ABOUT_MENU, SHARE_MENU, DONATION_MENU
from bot.constants.markup import button, keyboard
from bot.constants import key
from bot.utils import send_message
from core.logger import logger  # noqa


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, text.START, keyboard=keyboard.main_menu, link_preview=False)
    commands = [
        BotCommand("/start", "Начть работу"),
        BotCommand("/menu", "Перейти в главное меню"),
        BotCommand("/cancel", "Отменить текущее действие"),
        BotCommand("/stop", "Завершение работы"),
    ]
    await context.bot.set_my_commands(commands)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    await send_message(update, text.MAIN_MENU, keyboard=keyboard.main_menu)

    return state.MAIN_MENU


async def share_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    await send_message(update, text.SELECT_URL, keyboard=keyboard.share_menu)

    return state.MAIN_MENU


async def share_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    link = SHARE_MENU[update.callback_query.data]
    link_button = Button(f'Перейти {link.get(key.DESCRIPTION)}', url=link.get(key.LINK))
    link_keyboard = Keyboard([
        [link_button],
        [button.share_menu],
    ])
    message = f'Ссылка: {link.get(key.LINK)}'
    await send_message(update, message, keyboard=link_keyboard)

    return state.MAIN_MENU


async def donation_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""
    await send_message(update, text.ABOUT, keyboard=keyboard.donation_menu)

    return state.MAIN_MENU


async def donation_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    option = DONATION_MENU[update.callback_query.data]
    option_keyboard = Keyboard([[button.donation_menu]])
    await send_message(update, option.get(key.DESCRIPTION), keyboard=option_keyboard)

    return state.MAIN_MENU


async def about_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""
    await send_message(update, text.ABOUT, keyboard=keyboard.about_menu)

    return state.MAIN_MENU


async def about_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    option = ABOUT_MENU[update.callback_query.data]
    option_keyboard = Keyboard([[button.about_menu]])
    await send_message(update, option.get(key.DESCRIPTION), keyboard=option_keyboard)

    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """FILL ME"""
    await update.message.reply_text(text.STOP)

    return ConversationHandler.END
