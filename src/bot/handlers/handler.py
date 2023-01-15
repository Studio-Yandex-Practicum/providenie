from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu
from bot.conversations.fund_application import fund_application
from bot.handlers.chat_handler import chat_conv
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    chat_conv,
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
        fund_application, pattern="^" + str(states.ABOUT) + "$"
    ),
    CallbackQueryHandler(menu.end, pattern="^" + str(states.END) + "$"),
    CallbackQueryHandler(menu.end, pattern="^" + str(states.SENT) + "$"),
]

conv_handler = ConversationHandler(
    name="conv_handler",
    allow_reentry=True,
    entry_points=[CommandHandler("start", menu.start)],
    states={
        states.SELECTING_ACTION: selection_handlers,
        states.STOPPING: [CommandHandler("start", menu.start)],
    },
    fallbacks=[CommandHandler("stop", menu.stop)],
)
