from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu
from bot.handlers.volunteer import add_volunteer_conv

from ..constans import fund_app_constans
from .join_to_fond import conv_handler_join_to_fond


selection_handlers = [
    CallbackQueryHandler(
        menu.select_chat, pattern="^" + str(states.CHATS) + "$"
    ),
    CallbackQueryHandler(
        menu.request, pattern="^" + str(states.REQUEST) + "$"
    ),
    add_volunteer_conv,
    CallbackQueryHandler(
        menu.talk_friends, pattern="^" + str(states.TALK) + "$"
    ),
    CallbackQueryHandler(
        menu.give_donation, pattern="^" + str(states.DONATION) + "$"
    ),
    CallbackQueryHandler(
        menu.get_events, pattern="^" + str(states.EVENTS) + "$"
    ),
    CallbackQueryHandler(
        menu.ask_question, pattern="^" + str(states.QUESTION) + "$"
    ),
    CallbackQueryHandler(
        menu.start,
        pattern="^" + str(fund_app_constans.GO_MAIN_MENU) + "$"
    ),
    # CallbackQueryHandler(
    #     , pattern="^" + str(states.ABOUT) + "$"
    # ),
    CallbackQueryHandler(menu.end, pattern="^" + str(states.END) + "$"),
    CallbackQueryHandler(menu.end, pattern="^" + str(states.SENT) + "$"),
]

conv_handler = ConversationHandler(
    name="conv_handler",
    allow_reentry=True,
    entry_points=[CommandHandler("start", menu.start)],
    states={
        states.SELECTING_ACTION: selection_handlers,
        fund_app_constans.START_JOIN_TO_FOND: [conv_handler_join_to_fond],
        fund_app_constans.RETURN_FROM_JOIN_TO_FOND: selection_handlers,
        states.STOPPING: [CommandHandler("start", menu.start)],
    },
    fallbacks=[CommandHandler("stop", menu.stop)],
)
