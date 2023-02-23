from telegram.ext import (
    CallbackQueryHandler, CommandHandler,
    ConversationHandler, MessageHandler, filters
)

from bot.constants import callbacks, states
from bot.constants.keys import FORM, INPUT, SELECT
from bot.conversations import form_application, main_application


form_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(form_application.show_menu, pattern=fr"^{FORM}_\S*$")],
    states={
        states.CHOOSING: [
            CallbackQueryHandler(form_application.confirm_selection, pattern=fr"^{SELECT}_\S*$"),
            CallbackQueryHandler(form_application.ask_input, pattern=fr"^{INPUT}_\S*$"),
            CallbackQueryHandler(form_application.show_data, pattern=callbacks.SHOW_INFO),
        ],
        states.CONFIRMATION: [
            CallbackQueryHandler(form_application.ask_input, pattern=callbacks.START_DATA_COLLECTION),
            CallbackQueryHandler(form_application.edit_input, pattern=callbacks.INFO_CHANGE),
        ],
        states.TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_application.save_input)],
    },
    fallbacks=[MessageHandler(filters.Regex("^END$"), main_application.done)],
    # map_to_parent={
    #     # Return to top level menu
    #     states.BACK: states.MAIN_MENU,
    #     # End conversation altogether
    #     states.END: states.END,
    # },
    allow_reentry=True,
)


main_menu_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", main_application.start),
        CallbackQueryHandler(main_application.start, pattern=callbacks.BACK)
    ],
    states={
        states.MAIN_MENU: [
            form_conversation_handler,
            CallbackQueryHandler(main_application.tell_friend, pattern=callbacks.MENU_TELL_FRIEND),
            CallbackQueryHandler(main_application.give_link, pattern=r"^TELL_\S*$"),
            CallbackQueryHandler(main_application.give_donation, pattern=callbacks.MENU_GIVE_MONEY),
            CallbackQueryHandler(main_application.start, pattern=callbacks.MENU_ASK_Q),
            CallbackQueryHandler(main_application.show_about, pattern=callbacks.MENU_ABOUT),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), main_application.done)],
    allow_reentry=True,
)
