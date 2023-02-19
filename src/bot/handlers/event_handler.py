from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys as key
from bot import states as state
from bot.conversations import main_menu


event_conv = ConversationHandler(
    name="event_conv",
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(main_menu.get_events, pattern="^" + key.EVENTS + "$")
    ],
    states={
        state.STOPPING: [CallbackQueryHandler(
            main_menu.end_second_level, pattern="^" + str(key.END) + "$"
        )]
    },
    fallbacks=[
        CommandHandler("stop", main_menu.stop),
    ],
)
