from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import states
from bot.conversations import menu
from bot.conversations.parents_chat import chat_edit_data, chat_get_data
from bot.conversations.parents_chat.chat_entry import enter_chat
from bot.conversations.parents_chat.chat_main_menu import select_chat, chat_end
from bot.conversations.parents_chat.chat_send_email import (
    chat_end_sending,
    chat_send_email,
)


chat_edit_conv = ConversationHandler(
    name="chat_edit_conv",
    entry_points=[
        CallbackQueryHandler(
            chat_edit_data.chat_select_field,
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
                chat_edit_data.chat_edit_data,
                pattern="^(?!" + str(states.END) + ").*$",
            ),
        ],
        states.CHAT_TYPING: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_edit_data.chat_save_input
            )
        ],
        states.CHAT_SEND: [
            CallbackQueryHandler(
                chat_edit_data.chat_end_editing,
                pattern="^" + str(states.END) + "$",
            ),
            CallbackQueryHandler(
                chat_end_sending, pattern="^" + str(states.SENT) + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            chat_edit_data.chat_end_editing,
            pattern="^" + str(states.END) + "$",
        ),
        CallbackQueryHandler(
            chat_end_sending, pattern="^" + str(states.SENT) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.END: states.CHAT_SHOWING,
        states.SENT: states.STOPPING,
        states.STOPPING: states.END,
    },
)


chat_get_conv = ConversationHandler(
    name="chat_get_conv",
    entry_points=[
        CallbackQueryHandler(
            chat_get_data.entering_chat,
            pattern="^" + str(states.ENTRY_CHAT) + "$",
        )
    ],
    states={
        states.ENTERING_CHAT: [
            CallbackQueryHandler(
                enter_chat,
                pattern="^" + str(states.ENTRY_CHAT) + "$",
            )
        ],
        states.CHAT_GETTING_PARENTS_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_parents_name,
            )
        ],
        states.CHAT_GETTING_PARENTS_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_parents_phone,
            ),
        ],
        states.CHAT_GETTING_CHILD_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_name,
            )
        ],
        states.CHAT_GETTING_CHILD_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_birthday,
            )
        ],
        states.CHAT_GETTING_CHILD_PLACE_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_place_birthday,
            )
        ],
        states.CHAT_GETTING_CHILD_TERM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_term,
            )
        ],
        states.CHAT_GETTING_CHILD_WEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_weight,
            )
        ],
        states.CHAT_GETTING_CHILD_HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_height,
            )
        ],
        states.CHAT_GETTING_CHILD_DIAGNOSE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_diagnose,
            )
        ],
        states.CHAT_GETTING_CHILD_OPERATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_child_operation,
            )
        ],
        states.CHAT_GETTING_ABOUT_FOND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.chat_getting_about_fond,
            )
        ],
        states.CHAT_SHOWING: [chat_edit_conv],
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(states.END) + "$"
        ),
        CallbackQueryHandler(select_chat, pattern="^" + str(states.CHATS) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.CHATS: states.SELECTING_CHAT,
        states.END: states.END,
        states.STOPPING: states.STOPPING,
    },
)


chat_handlers = [
    CallbackQueryHandler(
        enter_chat,
        pattern=(
            "^" + str(states.CHAT_BABY) + "$|^" + str(states.CHAT_CHILD) + "$|"
            "^" + str(states.CHAT_RETINOPATIA) + "$|^" + str(states.CHAT_SHUNTATA) + "$|"
            "^" + str(states.CHAT_GRANDMOTHERS) + "$|^" + str(states.CHAT_CRY) + "$|"
            "^" + str(states.CHAT_ANGELS) + "$|^" + str(states.CHAT_RETINOPATIA_4_5) + "$|"
            "^" + str(states.CHAT_PROBLEMS) + "$|^" + str(states.CHAT_REHABILITATION) + "$|"
            "^" + str(states.CHAT_TELEGRAM) + "$"
        ),
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
