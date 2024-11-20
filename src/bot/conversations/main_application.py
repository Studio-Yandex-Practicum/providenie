from telegram import BotCommandScopeChat, Update
from telegram import InlineKeyboardMarkup as Keyboard
from telegram.ext import ContextTypes, ConversationHandler

from app.core.db import get_async_session
from app.models.db_utils import create_or_update_user, get_user_by_tg_id

from bot.constants import button, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.core.logger import logger  # noqa
from bot.utils import get_menu_buttons, send_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a welcome message to the user."""
    tg_user = update.effective_user

    async for session in get_async_session():
        db_user = await get_user_by_tg_id(session, tg_user.id)

        if db_user and db_user.is_block:
            await send_message(
                update,
                text.MESSAGE_BLOCK_ACCOUNT,
            )
            return ConversationHandler.END

        await create_or_update_user(session, tg_user)

        if db_user and not db_user.is_active:
            await send_message(
                update,
                text.MESSAGE_RECOVERY_ACCOUNT,
            )
        else:
            await send_message(update, text.START, link_preview=False)

    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the main menu to the user and set the bot's commands."""
    await context.bot.set_my_commands(
        [button.START_CMD, button.STOP_CMD],
        scope=BotCommandScopeChat(update.effective_chat.id),
    )
    await send_message(
        update,
        text.MAIN_MENU,
        keyboard=Keyboard([*get_menu_buttons(ALL_MENU)]),
    )

    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End the conversation."""
    await send_message(update, text.STOP)

    return ConversationHandler.END
