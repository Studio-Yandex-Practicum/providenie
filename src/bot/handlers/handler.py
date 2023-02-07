from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys as key
from bot import states as state
from bot.conversations import menu
from bot.handlers.about_fund import about_fund_conv
from bot.handlers.ask_question import ask_question_conv
from bot.handlers.chat_handler import chat_conv
from bot.handlers.join_to_fund import conv_handler_join_to_fund
from bot.handlers.tell_about_fund import tell_about_fund_conv
from bot.handlers.volunteer import add_volunteer_conv


selection_handlers = [
    chat_conv,
    conv_handler_join_to_fund,
    add_volunteer_conv,
    about_fund_conv,
    CallbackQueryHandler(menu.give_donation, pattern="^" + key.DONATION + "$"),
    CallbackQueryHandler(menu.get_events, pattern="^" + key.EVENTS + "$"),
    ask_question_conv,
    tell_about_fund_conv,
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
