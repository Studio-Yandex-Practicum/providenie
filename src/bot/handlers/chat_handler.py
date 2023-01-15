from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import states
from bot.conversations import menu
from bot.conversations.parents_chat.chat_edit_data import (
    chat_edit_data,
    chat_end_editing,
    save_chat_input,
    select_chat_field,
)
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
from bot.conversations.parents_chat.chat_get_data import (
    chat_getting_about_fond,
    chat_getting_child_birthday,
    chat_getting_child_diagnose,
    chat_getting_child_height,
    chat_getting_child_name,
    chat_getting_child_operation,
    chat_getting_child_place_birthday,
    chat_getting_child_term,
    chat_getting_child_weight,
    chat_getting_date_address,
    chat_getting_parents_name,
    chat_getting_parents_phone,
    entering_chat,
)
from bot.conversations.parents_chat.chat_main_menu import select_chat
from bot.conversations.parents_chat.chat_send_email import (
    chat_end_sending,
    chat_send_email,
)


chat_edit_conv = ConversationHandler(
    name="chat_edit_conv",
    entry_points=[
        CallbackQueryHandler(
            select_chat_field,
            pattern="^" + str(states.CHAT_DATA_EDIT) + "$",
        ),
        CallbackQueryHandler(
            chat_send_email,
            pattern="^" + str(states.CHAT_SEND) + "$",
        ),
    ],
    states={
        states.CHAT_FEATURE: [
            CallbackQueryHandler(
                chat_edit_data,
                pattern="^(?!" + str(states.END) + ").*$",
            ),
        ],
        states.CHAT_TYPING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_chat_input)
        ],
        states.CHAT_SEND: [
            CallbackQueryHandler(
                chat_end_editing, pattern="^" + str(states.END) + "$"
            ),
            CallbackQueryHandler(
                chat_end_sending, pattern="^" + str(states.CHAT_SEND) + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            chat_end_editing, pattern="^" + str(states.END) + "$"
        ),
        CallbackQueryHandler(
            chat_end_sending, pattern="^" + str(states.CHAT_SEND) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.END: states.SELECTING_CHAT,
        states.CHAT_SEND: states.STOPPING,
        states.STOPPING: states.END,
    },
)


chat_get_conv = ConversationHandler(
    name="chat_get_conv",
    entry_points=[
        CallbackQueryHandler(
            entering_chat,
            pattern="^" + str(states.ENTRY_CHAT) + "$",
        )
    ],
    states={
        states.ENTERING_CHAT: [
            CallbackQueryHandler(
                enter_chat_baby,
                pattern="^" + str(states.ENTRY_CHAT) + "$",
            )
        ],
        states.CHAT_GETTING_PARENTS_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_parents_name
            )
        ],
        states.CHAT_GETTING_PARENTS_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_parents_phone
            )
        ],
        states.CHAT_GETTING_CHILD_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_name
            )
        ],
        states.CHAT_GETTING_CHILD_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_birthday
            )
        ],
        states.CHAT_GETTING_CHILD_PLACE_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_getting_child_place_birthday,
            )
        ],
        states.CHAT_GETTING_CHILD_TERM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_term
            )
        ],
        states.CHAT_GETTING_CHILD_WEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_weight
            )
        ],
        states.CHAT_GETTING_CHILD_HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_height
            )
        ],
        states.CHAT_GETTING_CHILD_DIAGNOSE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_diagnose
            )
        ],
        states.CHAT_GETTING_CHILD_OPERATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_child_operation
            )
        ],
        states.CHAT_GETTING_DATE_ADDRESS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_date_address
            )
        ],
        states.CHAT_GETTING_ABOUT_FOND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_getting_about_fond
            )
        ],
        states.CHAT_SHOWING: [chat_edit_conv],
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(states.END) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.END: states.SELECTING_CHAT,
        states.STOPPING: states.STOPPING,
    },
)


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
        enter_chat_telegram, pattern="^" + str(states.CHAT_TELEGRAM) + "$"
    ),
]

chat_conv = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(
            select_chat, pattern="^" + str(states.CHATS) + "$"
        )
    ],
    states={
        states.SELECTING_CHAT: chat_handlers,
        states.ENTERING_CHAT: [chat_get_conv],
    },
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
