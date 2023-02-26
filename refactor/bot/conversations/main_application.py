from telegram import BotCommand
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.constants.info.text import CANCEL_CMD, MENU_CMD, START_CMD, STOP_CMD
from bot.utils import get_menu_buttons, send_message
from core.logger import logger  # noqa


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user and set the bot's commands"""

    await send_message(update, text.START, link_preview=False)
    COMMANDS = [
        BotCommand('/start', START_CMD),
        BotCommand('/menu', MENU_CMD),
        BotCommand('/cancel', CANCEL_CMD),
        BotCommand('/stop', STOP_CMD),
    ]
    await context.bot.set_my_commands(COMMANDS)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the main menu to the user"""

    await send_message(update, text.MAIN_MENU, keyboard=Keyboard([*get_menu_buttons(ALL_MENU)]))

    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End the conversation"""

    await send_message(update, text.STOP)

    return ConversationHandler.END
