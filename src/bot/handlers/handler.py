from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu
from bot.handlers.ask_question import ask_question_conv
from bot.handlers.tell_about_fund import tell_about_fund_conv
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    CallbackQueryHandler(
        menu.select_chat, pattern="^" + str(states.CHATS) + "$"
    ),
    CallbackQueryHandler(
        menu.request, pattern="^" + str(states.REQUEST) + "$"
    ),
    add_volunteer_conv,
    tell_about_fund_conv,
    CallbackQueryHandler(
        menu.give_donation, pattern="^" + str(states.DONATION) + "$"
    ),
    CallbackQueryHandler(
        menu.get_events, pattern="^" + str(states.EVENTS) + "$"
    ),
    ask_question_conv,
    CallbackQueryHandler(menu.about, pattern="^" + str(states.ABOUT) + "$"),
    CallbackQueryHandler(
        menu.start, pattern="^" + str(states.START_OVER) + "$"
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
