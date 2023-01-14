from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu
from bot.conversations.parents_chat.chat_entry import (
    enter_chat_angels,
    enter_chat_baby,
    enter_chat_child,
    enter_chat_cry,
    enter_chat_grandmothers,
    enter_chat_problems,
    enter_chat_rehabilitation,
    enter_chat_retinopatia,
    enter_chat_retinopatia_4_5,
    enter_chat_shuntata,
    enter_chat_telegram,
)
from bot.conversations.parents_chat.chat_main_menu import select_chat


chat_handlers = [
    CallbackQueryHandler(
        enter_chat_child, pattern="^" + str(states.CHAT_CHILD) + "$"
    ),
    CallbackQueryHandler(
        enter_chat_baby, pattern="^" + str(states.CHAT_BABY) + "$"
    ),
    CallbackQueryHandler(
        enter_chat_retinopatia,
        pattern="^" + str(states.CHAT_RETINOPATIA) + "$",
    ),
    CallbackQueryHandler(
        enter_chat_shuntata, pattern="^" + str(states.CHAT_SHUNTATA) + "$"
    ),
    CallbackQueryHandler(
        enter_chat_grandmothers,
        pattern="^" + str(states.CHAT_GRANDMOTHERS) + "$",
    ),
    CallbackQueryHandler(
        enter_chat_cry, pattern="^" + str(states.CHAT_CRY) + "$"
    ),
    CallbackQueryHandler(
        enter_chat_angels, pattern="^" + str(states.CHAT_ANGELS) + "$"
    ),
    CallbackQueryHandler(
        enter_chat_retinopatia_4_5,
        pattern="^" + str(states.CHAT_RETINOPATIA_4_5) + "$",
    ),
    CallbackQueryHandler(
        enter_chat_problems, pattern="^" + str(states.CHAT_PROBLEMS) + "$"
    ),
    CallbackQueryHandler(
        enter_chat_rehabilitation,
        pattern="^" + str(states.CHAT_REHABILITATION) + "$",
    ),
    CallbackQueryHandler(
        enter_chat_telegram, pattern="^" + str(states.CHAT_TELECRAM) + "$"
    ),
]

chat_conv = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(
            select_chat, pattern="^" + str(states.CHATS) + "$"
        )
    ],
    states={states.SELECTING_CHAT: chat_handlers},
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(states.END) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.END: states.SELECTING_ACTION,
        states.STOPPING: states.STOPPING,
    },
)
