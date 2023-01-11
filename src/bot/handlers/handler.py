from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import constants as const
from bot.conversations import menu
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    add_volunteer_conv,
    CallbackQueryHandler(menu.end, pattern="^" + str(const.END) + "$"),
    CallbackQueryHandler(menu.end, pattern="^" + str(const.SENT) + "$"),
]

conv_handler = ConversationHandler(
    name="conv_handler",
    entry_points=[CommandHandler("start", menu.start)],
    states={
        const.SELECTING_ACTION: selection_handlers,
        const.STOPPING: [CommandHandler("start", menu.start)],
    },
    fallbacks=[CommandHandler("stop", menu.stop)],
)
