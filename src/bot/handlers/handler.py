from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys as key
from bot import states as state
from bot.conversations import menu
from bot.handlers.ask_question import ask_question_conv
from bot.handlers.chat_handler import chat_conv
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    chat_conv,
    CallbackQueryHandler(menu.request, pattern="^" + key.REQUEST + "$"),
    add_volunteer_conv,
    CallbackQueryHandler(menu.talk_friends, pattern="^" + key.TALK + "$"),
    CallbackQueryHandler(menu.give_donation, pattern="^" + key.DONATION + "$"),
    CallbackQueryHandler(menu.get_events, pattern="^" + key.EVENTS + "$"),
    ask_question_conv,
    CallbackQueryHandler(menu.about, pattern="^" + key.ABOUT + "$"),
    CallbackQueryHandler(menu.end, pattern="^" + str(key.END) + "$"),
    CallbackQueryHandler(menu.end, pattern="^" + key.SENT + "$"),
]

conv_handler = ConversationHandler(
    name="conv_handler",
    allow_reentry=True,
    entry_points=[CommandHandler("start", menu.start)],
    states={
        state.SELECTING_ACTION: selection_handlers,
        state.STOPPING: [CommandHandler("start", menu.start)],
        state.ENDING: [
            CallbackQueryHandler(menu.start, pattern="^" + str(key.END) + "$")
        ],
    },
    fallbacks=[CommandHandler("stop", menu.stop)],
)
