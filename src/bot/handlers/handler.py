from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu
from bot.handlers.ask_question import ask_question_conv
from bot.handlers.join_to_fund import conv_handler_join_to_fund
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    CallbackQueryHandler(
        menu.select_chat, pattern="^" + str(states.CHATS) + "$"
    ),
    conv_handler_join_to_fund,
    add_volunteer_conv,
    # CallbackQueryHandler(
    #     menu.request, pattern="^" + key.REQUEST + "$"
    # ),
    CallbackQueryHandler(
        menu.talk_friends, pattern="^" + str(states.TALK) + "$"
    ),
    CallbackQueryHandler(
        menu.give_donation, pattern="^" + str(states.DONATION) + "$"
    ),
    CallbackQueryHandler(
        menu.get_events, pattern="^" + str(states.EVENTS) + "$"
    ),
    ask_question_conv,
    CallbackQueryHandler(
        menu.about, pattern="^" + str(states.ABOUT) + "$"
    ),
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
