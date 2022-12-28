from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from .conversations.fund_application import fund_application
from .conversations.menu import (ask_question, end, get_events, give_donation,
                                 request, start, start_welcome, talk_friends)
from .conversations.parents_chat import (angels, chat_baby, chat_child, cry,
                                         end_second_level, grandmothers,
                                         problems, rethinopatia,
                                         rethinopatia_4_5, select_chat,
                                         shuntata, stop_nested, telegram_chat)
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
    CHAT,
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
) = map(chr, range(9, 21))

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
TYPING = map(chr, range(30, 31))

STOPPING, SHOWING = map(chr, range(31, 33))
END = ConversationHandler.END
(START_OVER, CURRENT_CHAT) = map(chr, range(19, 21))

chat_handlers = [
    CallbackQueryHandler(chat_child, pattern="^" + str(CHAT_CHILD) + "$"),
    CallbackQueryHandler(chat_baby, pattern="^" + str(CHAT_BABY) + "$"),
    CallbackQueryHandler(rethinopatia, pattern="^" + str(RETINOPATIA) + "$"),
    CallbackQueryHandler(shuntata, pattern="^" + str(SHUNTATA) + "$"),
    CallbackQueryHandler(grandmothers, pattern="^" + str(GRANDMOTHERS) + "$"),
    CallbackQueryHandler(cry, pattern="^" + str(CRY) + "$"),
    CallbackQueryHandler(angels, pattern="^" + str(ANGELS) + "$"),
    CallbackQueryHandler(
        rethinopatia_4_5, pattern="^" + str(RETINOPATIA_4_5) + "$"
    ),
    CallbackQueryHandler(problems, pattern="^" + str(PROBLEMS) + "$"),
    CallbackQueryHandler(
        telegram_chat, pattern="^" + str(TELECRAM_CHAT) + "$"
    ),
]

chat_conv = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(select_chat, pattern="^" + str(CHAT) + "$")
    ],
    states={SELECTING_CHAT: chat_handlers},
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
    chat_conv,
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
        SELECTING_CHAT: [chat_conv],
        STOPPING: [CommandHandler("start", start)],
    },
    fallbacks=[CommandHandler("end", end)],
)
