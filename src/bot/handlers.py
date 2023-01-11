from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler)

from .conversations.fund_application import fund_application
from .conversations.menu import (ask_question, end, get_events, give_donation,
                                 menu, request, select_chat, start,
                                 talk_friends)
from .conversations.volunteer_application import volunteer_application


(
    SELECTING_ACTION,
    CHATS,
    REQUEST,
    VOLUNTEER,
    TALK,
    DONATION,
    EVENTS,
    QUESTION,
    ABOUT,
) = map(chr, range(9))

STOPPING, SHOWING = map(chr, range(31, 33))
END = ConversationHandler.END
(START_OVER, CURRENT_CHAT) = map(chr, range(40, 42))

#   handlers главного меню
selection_handlers = [
    CallbackQueryHandler(start, pattern="^" + str("MAIN") + "$"),
    CallbackQueryHandler(select_chat, pattern="^" + str(CHATS) + "$"),
    CallbackQueryHandler(request, pattern="^" + str(REQUEST) + "$"),
    CallbackQueryHandler(
        volunteer_application, pattern="^" + str(VOLUNTEER) + "$"
    ),
    CallbackQueryHandler(talk_friends, pattern="^" + str(TALK) + "$"),
    CallbackQueryHandler(give_donation, pattern="^" + str(DONATION) + "$"),
    CallbackQueryHandler(get_events, pattern="^" + str(EVENTS) + "$"),
    CallbackQueryHandler(ask_question, pattern="^" + str(QUESTION) + "$"),
    CallbackQueryHandler(fund_application, pattern="^" + str(ABOUT) + "$"),
    CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
]

conv_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("menu", menu),
    ],
    states={
        SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
        SELECTING_ACTION: selection_handlers,
        STOPPING: [CommandHandler("start", start)],
    },
    fallbacks=[CommandHandler("end", end)],
)
