
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import button, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.core.logger import logger  # noqa
from bot.utils import get_menu_buttons, send_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user"""

    await send_message(update, text.START, link_preview=False)

    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the main menu to the user and set the bot's commands"""

    await context.bot.set_my_commands([button.START_CMD, button.STOP_CMD])
    await send_message(update, text.MAIN_MENU, keyboard=Keyboard([*get_menu_buttons(ALL_MENU)]))

    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End the conversation"""

    await send_message(update, text.STOP)

    return ConversationHandler.END
