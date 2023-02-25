from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
from bot.constants.info import text
from bot.constants.info.about import ABOUT_OPTIONS, SHARE_OPTIONS, DONATION_OPTIONS
from bot.constants.markup import button, keyboard
from bot.utils import send_message
from core.logger import logger  # noqa


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    await send_message(update, text.MSG_START, keyboard=keyboard.main_menu)

    return state.MAIN_MENU


async def share_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    await send_message(update, text.MSG_CHOOSE_URL, keyboard=keyboard.share_menu)

    return state.MAIN_MENU


async def share_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    link = SHARE_OPTIONS[update.callback_query.data]
    link_button = Button(f'Перейти {link.get("desc")}', url=link.get('url'))
    link_keyboard = Keyboard([
        [link_button],
        [button.share_menu],
    ])
    message = f'Ссылка: {link.get("url")}'
    await send_message(update, message, keyboard=link_keyboard)

    return state.MAIN_MENU


async def about_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""
    await send_message(update, text.MSG_INFO_ABOUT_FUND, keyboard=keyboard.about_menu)

    return state.MAIN_MENU


async def donation_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""
    await send_message(update, text.MSG_INFO_ABOUT_FUND, keyboard=keyboard.donation_menu)

    return state.MAIN_MENU


async def donation_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    option = DONATION_OPTIONS[update.callback_query.data]
    option_keyboard = Keyboard([[button.donation_menu]])
    await send_message(update, option.get('desc'), keyboard=option_keyboard)

    return state.MAIN_MENU


async def about_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FILL ME"""

    option = ABOUT_OPTIONS[update.callback_query.data]
    option_keyboard = Keyboard([[button.about_menu]])
    await send_message(update, option.get('desc'), keyboard=option_keyboard)

    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """FILL ME"""
    await update.message.reply_text("До скорых встреч!")

    return ConversationHandler.END
