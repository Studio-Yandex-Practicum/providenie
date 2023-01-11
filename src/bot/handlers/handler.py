from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    add_volunteer_conv,
    CallbackQueryHandler(menu.end, pattern="^" + str(states.END) + "$"),
    CallbackQueryHandler(menu.end, pattern="^" + str(states.SENT) + "$"),
]

conv_handler = ConversationHandler(
    name="conv_handler",
    entry_points=[CommandHandler("start", menu.start)],
    states={
        states.SELECTING_ACTION: selection_handlers,
        states.STOPPING: [CommandHandler("start", menu.start)],
    },
    fallbacks=[CommandHandler("stop", menu.stop)],
)
