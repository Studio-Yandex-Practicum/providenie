from telegram.ext import (
    CallbackQueryHandler, CommandHandler,
    ConversationHandler, MessageHandler, filters
)

from bot.constants import callbacks, states
from bot.constants.keys import FORM, INPUT, SELECT, SHARE, ABOUT
from bot.conversations import form_application, main_application


form_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(form_application.form_menu, pattern=fr"^{FORM}_\S*$")],
    states={
        states.CHOOSING: [
            CallbackQueryHandler(form_application.confirm_selection, pattern=fr"^{SELECT}_\S*$"),
            CallbackQueryHandler(form_application.ask_input, pattern=fr"^{INPUT}_\S*$"),
            CallbackQueryHandler(form_application.show_data, pattern=callbacks.INFO_SHOW),
        ],
        states.CONFIRMATION: [
            CallbackQueryHandler(form_application.ask_input, pattern=callbacks.INFO_COLLECT),
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
        CommandHandler("start", main_application.main_menu),
        CallbackQueryHandler(main_application.main_menu, pattern=callbacks.BACK)
    ],
    states={
        states.MAIN_MENU: [
            form_conversation_handler,
            CallbackQueryHandler(main_application.share_menu, pattern=callbacks.SHARE_INFO),
            CallbackQueryHandler(main_application.share_link, pattern=fr"^{SHARE}_\S*$"),
            CallbackQueryHandler(main_application.about_menu, pattern=callbacks.MENU_ABOUT),
            CallbackQueryHandler(main_application.about_option, pattern=fr"^{ABOUT}_\S*$"),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), main_application.done)],
    allow_reentry=True,
)
