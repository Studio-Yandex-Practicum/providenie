from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys as key
from bot import states as state
from bot.conversations import main_menu
from bot.handlers.about_handler import about_fund_conv
from bot.handlers.chat_handler import chat_conv
from bot.handlers.join_handler import conv_handler_join_to_fund
from bot.handlers.question_handler import ask_question_conv
from bot.handlers.share_links_handler import tell_about_fund_conv
from bot.handlers.volunteer_handler import add_volunteer_conv


selection_handlers = [
    chat_conv,
    conv_handler_join_to_fund,
    add_volunteer_conv,
    about_fund_conv,
    CallbackQueryHandler(
        main_menu.give_donation, pattern="^" + key.DONATION + "$"
    ),
    CallbackQueryHandler(main_menu.get_events, pattern="^" + key.EVENTS + "$"),
    ask_question_conv,
    tell_about_fund_conv,
    CallbackQueryHandler(main_menu.end, pattern="^" + str(key.END) + "$"),
    CallbackQueryHandler(main_menu.end, pattern="^" + key.SENT + "$"),
]

conv_handler = ConversationHandler(
    name="conv_handler",
    allow_reentry=True,
    entry_points=[CommandHandler("start", main_menu.start)],
    states={
        state.SELECTING_ACTION: selection_handlers,
        state.STOPPING: [CommandHandler("start", main_menu.start)],
        state.ENDING: [
            CallbackQueryHandler(
                main_menu.start, pattern="^" + str(key.END) + "$"
            )
        ],
    },
    fallbacks=[CommandHandler("stop", main_menu.stop)],
)
