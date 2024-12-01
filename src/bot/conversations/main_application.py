from telegram import BotCommandScopeChat, Update
from telegram import InlineKeyboardMarkup as Keyboard
from telegram.ext import ContextTypes, ConversationHandler

from app.core.db import get_async_session
from app.crud.user_tg import crud_user
from app.schemas.auth import UserCreate

from bot.constants import button, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.core.logger import logger  # noqa
from bot.utils import get_menu_buttons, send_message


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
        existing_user = await crud_user.get_one_by_attributes(
            filters={'tg_id': user_data['tg_id']},
            session=session,
        )
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
                pydantic_scheme_obj=new_user,
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
