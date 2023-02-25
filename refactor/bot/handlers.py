from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from bot.constants import callback, state
from bot.constants.key import ABOUT, FORM, ASK, SELECT, SHARE
from bot.conversations import form_application, main_application


form_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(form_application.form_menu, pattern=fr"^{FORM}_\S*$")],
    states={
        state.FORM_SELECTION: [
            CallbackQueryHandler(form_application.confirm_selection, pattern=fr"^{SELECT}_\S*$"),
        ],
        state.FORM_SUBMISSION: [
            CallbackQueryHandler(form_application.ask_input, pattern=callback.COLLECT_DATA),
            CallbackQueryHandler(form_application.edit_menu, pattern=callback.EDIT_MENU),
            CallbackQueryHandler(form_application.show_data, pattern=callback.SHOW_DATA),
            CallbackQueryHandler(form_application.send_data, pattern=callback.SEND_DATA),
        ],
        state.FORM_INPUT: [
            CallbackQueryHandler(form_application.ask_input, pattern=fr"^{ASK}_\S*$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, form_application.save_input),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^END$"), main_application.done)],
    allow_reentry=True,
)


main_menu_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", main_application.main_menu),
        CallbackQueryHandler(main_application.main_menu, pattern=callback.BACK)
    ],
    states={
        state.MAIN_MENU: [
            form_handler,
            CallbackQueryHandler(main_application.share_menu, pattern=callback.SHARE_INFO),
            CallbackQueryHandler(main_application.share_link, pattern=fr"^{SHARE}_\S*$"),
            CallbackQueryHandler(main_application.about_menu, pattern=callback.MENU_ABOUT),
            CallbackQueryHandler(main_application.about_option, pattern=fr"^{ABOUT}_\S*$"),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), main_application.done)],
    allow_reentry=True,
)
