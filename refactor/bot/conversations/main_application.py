from telegram import BotCommand
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.constants.info.text import (START_BOT, MENU_BOT,
                                     CANCEL_BOT, STOP_BOT)
from bot.utils import get_menu_buttons, send_message
from core.logger import logger  # noqa


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, text.START, link_preview=False)
    COMMANDS = [
        BotCommand("/start", START_BOT),
        BotCommand("/menu", MENU_BOT),
        BotCommand("/cancel", CANCEL_BOT),
        BotCommand("/stop", STOP_BOT),
    ]
    await context.bot.set_my_commands(COMMANDS)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await send_message(update, text.MAIN_MENU, keyboard=Keyboard([*get_menu_buttons(ALL_MENU)]))

    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await send_message(update, text.STOP)

    return ConversationHandler.END
