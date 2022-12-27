from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from .conversations.fund_application import fund_application
from .conversations.menu import (ask_question, end, get_events, give_donation,
                                 request, start, start_welcome, talk_friends)
from .conversations.parents_chat import (baby_surname, end_second_level,
                                         parents_surname, select_chat,
                                         stop_nested, telephone_number)
from .conversations.volunteer_application import volunteer_application


(
    SELECTING_ACTION,
    CHAT,
    REQUEST,
    VOLUNTEER,
    TALK,
    DONATION,
    EVENTS,
    QUESTION,
    ABOUT,
) = map(chr, range(9))

(
    SELECTING_CHAT,
    CHAT_BABY,
    CHAT_CHILD,
    SHUNTATA,
    RETINOPATIA,
    GRANDMOTHERS,
    CRY,
    ANGELS,
    RETINOPATIA_4_5,
    PROBLEMS,
    TELECRAM_CHAT,
) = map(chr, range(9, 20))


(
    PARENTS_SURNAME,
    TELEPHONE_NUMBER,
    BABY_SURNAME,
    DATE_OF_BIRTH,
    PLACE_OF_BIRTH,
    TERM_OF_BIRTH,
    WEIGHT,
    HEIGHT,
) = map(chr, range(21, 29))


STOPPING, SHOWING = map(chr, range(31, 33))
END = ConversationHandler.END
(START_OVER, CURRENT_CHAT) = map(chr, range(19, 21))


description_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            select_chat,
            pattern="^" + str(CHAT_BABY) + "$|^" + str(CHAT_CHILD) + "$|"
            "^" + str(RETINOPATIA) + "$|^" + str(SHUNTATA) + "$|"
            "^" + str(GRANDMOTHERS) + "$|^" + str(CRY) + "$|"
            "^" + str(ANGELS) + "$|"
            "^" + str(RETINOPATIA_4_5) + "$|"
            "^" + str(PROBLEMS) + "$|^" + str(TELECRAM_CHAT) + "$",
        )
    ],
    states={
        PARENTS_SURNAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, parents_surname)
        ],
        TELEPHONE_NUMBER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, telephone_number)
        ],
        BABY_SURNAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, baby_surname)
        ],
    },
    fallbacks=[
        CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
        CommandHandler("stop", stop_nested),
    ],
    map_to_parent={
        END: SELECTING_CHAT,
        STOPPING: STOPPING,
    },
)


selection_handlers = [
    description_conv,
    CallbackQueryHandler(start, pattern="^" + str("MAIN") + "$"),
    CallbackQueryHandler(select_chat, pattern="^" + str(CHAT) + "$"),
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
        CommandHandler("start_welcome", start_welcome),
    ],
    states={
        SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
        SELECTING_ACTION: selection_handlers,
        STOPPING: [CommandHandler("start", start)],
    },
    fallbacks=[CommandHandler("end", end)],
)
