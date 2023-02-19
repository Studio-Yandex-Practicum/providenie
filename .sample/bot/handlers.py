from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler
)

from .conversations import menu, parents_chat, fund_application, volunteer_application
from .import callbacks
from . import states


parents_chat_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(parents_chat.start, pattern=callbacks.MENU_CHAT)],
    states={
        states.CHAT_CHOOSING: [
            CallbackQueryHandler(parents_chat.confirm_selection, pattern="^CHAT_SELECT_\S*$"),
            CallbackQueryHandler(parents_chat.ask_for_input, pattern="^INFO_\S*$"),
            CallbackQueryHandler(parents_chat.show_data, pattern=callbacks.SHOW),
        ],
        states.CHAT_CONFIRMATION: [
            CallbackQueryHandler(parents_chat.ask_for_input, pattern=callbacks.START_DATA_COLLECTION),
            CallbackQueryHandler(parents_chat.change_input, pattern=callbacks.INFO_CHANGE),
            CallbackQueryHandler(parents_chat.start, pattern=callbacks.MENU_CHAT),
        ],
        states.CHAT_TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, parents_chat.save_input)],
        states.CHAT_SHOWING: [MessageHandler(filters.TEXT & ~filters.COMMAND, parents_chat.show_data),],
    },
    fallbacks=[MessageHandler(filters.Regex("^END$"), menu.done)],
    map_to_parent={
            # Return to top level menu
            states.BACK: states.LEVEL_MENU,
            # End conversation altogether
            states.END: states.END,
        },
)

fond_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(fund_application.start, pattern=callbacks.MENU_APP_FOND)],
    states={
        states.FOND_CHOOSING: [
            CallbackQueryHandler(fund_application.confirm_selection, pattern="^FOND_SELECT_\S*$"),
            CallbackQueryHandler(fund_application.ask_for_input, pattern="^INFO_\S*$"),
            CallbackQueryHandler(fund_application.show_data, pattern=callbacks.SHOW),
        ],
        states.FOND_CONFIRMATION: [
            CallbackQueryHandler(fund_application.ask_for_input, pattern=callbacks.START_DATA_COLLECTION),
            CallbackQueryHandler(fund_application.change_input, pattern=callbacks.INFO_CHANGE),
            CallbackQueryHandler(fund_application.start, pattern=callbacks.MENU_APP_FOND),
        ],
        states.FOND_TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, fund_application.save_input)],
        states.FOND_SHOWING: [MessageHandler(filters.TEXT & ~filters.COMMAND, fund_application.show_data),],
    },
    fallbacks=[MessageHandler(filters.Regex("^END$"), menu.done)],
    map_to_parent={
            # Return to top level menu
            states.BACK: states.LEVEL_MENU,
            # End conversation altogether
            states.END: states.END,
        },
)

volonter_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(volunteer_application.start, pattern=callbacks.MENU_VOLONTER)],
    states={
        states.VOLONTER_CHOOSING: [
            CallbackQueryHandler(volunteer_application.ask_for_input, pattern="^VOLONTER_INFO_\S*$"),
            CallbackQueryHandler(volunteer_application.show_data, pattern=callbacks.SHOW),
        ],
        states.VOLONTER_CONFIRMATION: [
            CallbackQueryHandler(volunteer_application.ask_for_input, pattern=callbacks.START_DATA_COLLECTION),
            CallbackQueryHandler(volunteer_application.change_input, pattern=callbacks.INFO_CHANGE),
            CallbackQueryHandler(menu.start, pattern=callbacks.BACK),
        ],
        states.VOLONTER_TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, volunteer_application.save_input)],
        states.VOLONTER_SHOWING: [MessageHandler(filters.TEXT & ~filters.COMMAND, volunteer_application.show_data),],
    },
    fallbacks=[MessageHandler(filters.Regex("^END$"), menu.done)],
    map_to_parent={
            # Return to top level menu
            states.BACK: states.LEVEL_MENU,
            # End conversation altogether
            states.END: states.END,
        },
)

main_menu_handler = ConversationHandler(
    entry_points=[CommandHandler("start", menu.start)],
    states={
        states.LEVEL0: [
            CallbackQueryHandler(menu.start, pattern=callbacks.BACK),
        ],
        states.LEVEL_MENU: [
            CallbackQueryHandler(menu.start, pattern=callbacks.BACK),
            parents_chat_handler,
            fond_handler,
            volonter_handler,
            CallbackQueryHandler(menu.tell_friend, pattern=callbacks.MENU_TELL_FRIEND),
            CallbackQueryHandler(menu.give_link, pattern="^TELL_\S*$"),
            CallbackQueryHandler(menu.give_donation, pattern=callbacks.MENU_GIVE_MONEY),
            CallbackQueryHandler(menu.start, pattern=callbacks.MENU_ASK_Q),
            CallbackQueryHandler(menu.show_about, pattern=callbacks.MENU_ABOUT),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), menu.done)],
    allow_reentry=True,
)
