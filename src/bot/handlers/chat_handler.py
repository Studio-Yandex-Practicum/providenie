from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import keys as key
from bot import states as state
from bot.conversations import main_menu
from bot.conversations.parents_chat import chat_edit_data, chat_get_data
from bot.conversations.parents_chat.chat_entry import enter_chat
from bot.conversations.parents_chat.chat_main_menu import select_chat
from bot.conversations.parents_chat.chat_send_email import (
    chat_end_sending,
    chat_send_email,
)


chat_edit_conv = ConversationHandler(
    name="chat_edit_conv",
    entry_points=[
        CallbackQueryHandler(
            chat_edit_data.chat_select_field,
            pattern="^" + state.CHAT_DATA_EDIT + "$",
        ),
        CallbackQueryHandler(
            chat_send_email,
            pattern="^" + state.CHAT_SEND + "$",
        ),
    ],
    states={
        state.CHAT_FEATURE: [
            CallbackQueryHandler(
                chat_edit_data.chat_edit_data,
                pattern="^(?!" + str(key.END) + ").*$",
            ),
        ],
        state.CHAT_TYPING: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, chat_edit_data.chat_save_input
            )
        ],
        state.CHAT_SEND: [
            CallbackQueryHandler(
                chat_edit_data.chat_end_editing,
                pattern="^" + str(key.END) + "$",
            ),
            CallbackQueryHandler(
                chat_end_sending, pattern="^" + key.SENT + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            chat_edit_data.chat_end_editing,
            pattern="^" + str(key.END) + "$",
        ),
        CallbackQueryHandler(chat_end_sending, pattern="^" + key.SENT + "$"),
        CommandHandler("stop", main_menu.stop_nested),
    ],
    map_to_parent={
        key.END: state.CHAT_SHOWING,
        key.SENT: state.STOPPING,
        state.STOPPING: key.END,
    },
)


chat_get_conv = ConversationHandler(
    name="chat_get_conv",
    entry_points=[
        CallbackQueryHandler(
            chat_get_data.ask_full_name,
            pattern="^" + key.ENTRY_CHAT + "$",
        )
    ],
    states={
        state.ENTERING_CHAT: [
            CallbackQueryHandler(
                enter_chat,
                pattern="^" + key.ENTRY_CHAT + "$",
            )
        ],
        state.CHAT_GETTING_PARENTS_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_phone_number,
            )
        ],
        state.CHAT_GETTING_PARENTS_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_full_name_child,
            ),
        ],
        state.CHAT_GETTING_CHILD_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_child_birthday,
            )
        ],
        state.CHAT_GETTING_CHILD_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_place_birthday,
            )
        ],
        state.CHAT_GETTING_CHILD_PLACE_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_child_term,
            )
        ],
        state.CHAT_GETTING_CHILD_TERM: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_child_weight,
            )
        ],
        state.CHAT_GETTING_CHILD_WEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_child_height,
            )
        ],
        state.CHAT_GETTING_CHILD_HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_child_diagnose,
            )
        ],
        state.CHAT_GETTING_CHILD_DIAGNOSE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_child_operation,
            )
        ],
        state.CHAT_GETTING_CHILD_OPERATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.ask_about_fond,
            )
        ],
        state.CHAT_GETTING_ABOUT_FOND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                chat_get_data.display_entered_value,
            )
        ],
        state.CHAT_SHOWING: [chat_edit_conv],
    },
    fallbacks=[
        CallbackQueryHandler(
            main_menu.end_second_level, pattern="^" + str(key.END) + "$"
        ),
        CallbackQueryHandler(select_chat, pattern="^" + key.CHATS + "$"),
        CommandHandler("stop", main_menu.stop_nested),
    ],
    map_to_parent={
        key.CHATS: state.SELECTING_CHAT,
        key.END: key.END,
        state.STOPPING: state.STOPPING,
    },
)


chat_handlers = [
    CallbackQueryHandler(enter_chat, pattern=r"^CHAT_SELECT_\S*$")
]

chat_conv = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(select_chat, pattern="^" + str(key.CHATS) + "$")
    ],
    states={
        state.SELECTING_CHAT: chat_handlers,
        state.ENTERING_CHAT: [chat_get_conv],
    },
    fallbacks=[
        CallbackQueryHandler(
            main_menu.end_second_level, pattern="^" + str(key.END) + "$"
        ),
        CommandHandler("stop", main_menu.stop_nested),
    ],
    map_to_parent={
        key.END: state.SELECTING_ACTION,
        state.STOPPING: state.STOPPING,
    },
)
