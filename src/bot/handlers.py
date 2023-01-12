from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

# from .conversations.fund_application import fund_application
from .conversations.menu import (
    about,
    ask_question,
    end,
    get_events,
    give_donation,
    menu,
    request,
    select_chat,
    social_link,
    start,
    talk_friends,
)
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

(
    SELECTING_MEDIA,
    WEBSITE,
    VK,
    INSTAGRAM,
    FACEBOOK,
    TG_CHANNEL,
    TG_BOT,
) = map(chr, range(9, 16))

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
    CallbackQueryHandler(about, pattern="^" + str(ABOUT) + "$"),
    CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
]

media_handlers = [
    CallbackQueryHandler(
        social_link,
        pattern=(
            f"^{str(WEBSITE)}$|^"
            + f"{str(VK)}$|^"
            + f"{str(INSTAGRAM)}$|^"
            + f"{str(FACEBOOK)}$|^"
            + f"{str(TG_CHANNEL)}$|^"
            + f"{str(TG_BOT)}$"
        ),
    ),
    # CallbackQueryHandler(about, pattern="^" + str(START_OVER) + "$"),
    CallbackQueryHandler(about, pattern="^" + str(END) + "$"),
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
        SELECTING_MEDIA: media_handlers,
        STOPPING: [CommandHandler("start", start)],
    },
    fallbacks=[CommandHandler("end", end)],
)
