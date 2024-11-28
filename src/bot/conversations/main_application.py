from sqlalchemy import select
from telegram import BotCommandScopeChat, Update
from telegram import InlineKeyboardMarkup as Keyboard
from telegram.ext import ContextTypes, ConversationHandler

from src.app.core.db import get_async_session
from src.app.crud.user_tg import crud_user
from src.app.models.models import UserTG
from src.app.schemas.auth import UserCreate
from src.bot.constants import button, state
from src.bot.constants.info import text
from src.bot.constants.info.menu import ALL_MENU
from src.bot.core.logger import logger  # noqa
from src.bot.utils import get_menu_buttons, send_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a welcome message to the user."""
    tg_user = update.effective_user
    user_data = {
        'tg_id': str(tg_user.id),
        'first_name': tg_user.first_name or 'Unknown',
        'last_name': tg_user.last_name or 'Unknown',
        'user_name': tg_user.username,
    }

    async for session in get_async_session():
        result = await session.execute(
            select(UserTG).where(UserTG.tg_id == user_data['tg_id']),
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            if existing_user.is_block:
                await send_message(
                    update,
                    text.MESSAGE_BLOCK_ACCOUNT,
                    link_preview=False,
                )
                return None
        else:
            new_user = UserCreate(**user_data)
            await crud_user.create(
                pydantic_scheme_user=new_user,
                session=session,
            )
            await send_message(
                update,
                text.MESSAGE_WELCOME,
                link_preview=False,
            )

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
