from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import keys as key
from bot import states as state
from bot.conversations import joining_volunteer as volunteer
from bot.conversations import main_menu


edit_volunteer_conv = ConversationHandler(
    name="edit_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.display_menu_editing_entered_value,
            pattern="^" + key.EDIT_VOLUNTEER + "$",
        ),
        CallbackQueryHandler(
            volunteer.send_email_to_curator,
            pattern="^" + key.SEND_VOLUNTEER + "$",
        ),
    ],
    states={
        state.VOLUNTEER_FEATURE: [
            CallbackQueryHandler(
                volunteer.ask_new_value,
                pattern="^(?!" + str(key.END) + ").*$",
            ),
        ],
        state.TYPING_VOLUNTEER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.save_new_value
            )
        ],
        state.VOLUNTEER_SENT: [
            CallbackQueryHandler(
                volunteer.display_all_new_entered_value,
                pattern="^" + str(key.END) + "$",
            ),
            CallbackQueryHandler(
                volunteer.return_to_main_menu_after_sending_value,
                pattern="^" + key.SENT + "$",
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            volunteer.display_all_new_entered_value,
            pattern="^" + str(key.END) + "$",
        ),
        CallbackQueryHandler(
            volunteer.return_to_main_menu_after_sending_value,
            pattern="^" + key.SENT + "$",
        ),
        CommandHandler("stop", main_menu.stop_nested),
    ],
    map_to_parent={
        key.END: state.SHOWING_VOLUNTEER,
        key.SENT: state.STOPPING,
        state.STOPPING: key.END,
    },
)

add_volunteer_conv = ConversationHandler(
    name="add_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.start_menu,
            pattern="^" + key.ADD_VOLUNTEER + "$",
        )
    ],
    states={
        state.ADDING_VOLUNTEER: [
            CallbackQueryHandler(
                volunteer.ask_full_name,
                pattern="^" + key.VOLUNTEER + "$",
            )
        ],
        state.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.ask_birthday
            )
        ],
        state.ADDING_BIRTHDAY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, volunteer.ask_city)
        ],
        state.ADDING_CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.ask_phone_number
            )
        ],
        state.ADDING_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.ask_email
            )
        ],
        state.ADDING_EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.ask_help_option
            )
        ],
        state.ADDING_MESSAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.save_help_option
            ),
            CommandHandler("skip", volunteer.save_empty_help_option),
        ],
        state.SHOWING_VOLUNTEER: [edit_volunteer_conv],
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
