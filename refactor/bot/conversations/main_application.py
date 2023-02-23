from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import buttons, keyboards, states
from bot.constants.info.about import ABOUT_OPTIONS
from bot.constants.info.share import SHARE_LINKS
from bot.utils import send_message
from core.logger import logger  # noqa


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, 'Сообщение в главном меню', keyboard=keyboards.main_menu)
    return states.MAIN_MENU


async def share_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, 'Выбрать чем поделиться:', keyboard=keyboards.share_menu)
    return states.MAIN_MENU


async def share_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = SHARE_LINKS[update.callback_query.data]
    link_button = Button(f'Перейти {link.get("desc")}', url=link.get('url'))
    link_keyboard = Keyboard([
        [link_button],
        [buttons.share_menu],
    ])
    message = f'Ссылка: {link.get("url")}'

    await send_message(update, message, keyboard=link_keyboard)
    return states.MAIN_MENU


async def about_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, 'Информация о фонде: почитайте здесь', keyboard=keyboards.about_menu)
    return states.MAIN_MENU


async def about_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    option = ABOUT_OPTIONS[update.callback_query.data]
    option_keyboard = Keyboard([[buttons.about_menu]])
    await send_message(update, option.get('desc'), keyboard=option_keyboard)
    return states.MAIN_MENU


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    await update.message.reply_text("Until next time!")

    return ConversationHandler.END
