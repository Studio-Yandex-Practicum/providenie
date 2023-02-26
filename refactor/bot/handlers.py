from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from bot.constants import callback, key, state
from bot.conversations import (form_application, main_application,
                               menu_application)


form_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(form_application.start_form, pattern=callback.START_FORM)],
    states={
        state.FORM_SUBMISSION: [
            CallbackQueryHandler(form_application.edit_menu, pattern=callback.EDIT_MENU),
            CallbackQueryHandler(form_application.show_data, pattern=callback.SHOW_DATA),
            CallbackQueryHandler(form_application.send_data, pattern=callback.SEND_DATA),
        ],
        state.FORM_INPUT: [
            CallbackQueryHandler(form_application.ask_input, pattern=fr"^{key.ASK}_\S*$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, form_application.save_input),
        ],
    },
    fallbacks=[],
    allow_reentry=True,
)


main_menu_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', main_application.start),
        CallbackQueryHandler(main_application.main_menu, pattern=callback.BACK)
    ],
    states={
        state.MAIN_MENU: [
            form_handler,
            CallbackQueryHandler(menu_application.show_menu, pattern=fr"^{key.MENU}_\S*$"),
            CallbackQueryHandler(menu_application.show_option, pattern=fr"^{key.OPTION}_\S*$"),
        ],
    },
    fallbacks=[
        CommandHandler('menu', main_application.main_menu),
        CommandHandler('cancel', main_application.main_menu),
        CommandHandler('stop', main_application.stop),
    ],
    allow_reentry=True,
)
