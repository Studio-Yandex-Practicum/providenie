from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import keys as key
from bot import states as state
from bot.conversations import menu
from bot.conversations import volunteer_application as volunteer


edit_volunteer_conv = ConversationHandler(
    name="edit_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.select_volunteer_field,
            pattern="^" + key.EDIT_VOLUNTEER + "$",
        ),
        CallbackQueryHandler(
            volunteer.send_email,
            pattern="^" + key.SEND_VOLUNTEER + "$",
        ),
    ],
    states={
        state.VOLUNTEER_FEATURE: [
            CallbackQueryHandler(
                volunteer.ask_volunteer,
                pattern="^(?!" + str(key.END) + ").*$",
            ),
        ],
        state.TYPING_VOLUNTEER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.save_volunteer_input
            )
        ],
        state.VOLUNTEER_SENT: [
            CallbackQueryHandler(
                volunteer.end_editing, pattern="^" + str(key.END) + "$"
            ),
            CallbackQueryHandler(
                volunteer.end_sending, pattern="^" + key.SENT + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            volunteer.end_editing, pattern="^" + str(key.END) + "$"
        ),
        CallbackQueryHandler(
            volunteer.end_sending, pattern="^" + key.SENT + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
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
            volunteer.add_volunteer,
            pattern="^" + key.ADD_VOLUNTEER + "$",
        )
    ],
    states={
        state.ADDING_VOLUNTEER: [
            CallbackQueryHandler(
                volunteer.adding_volunteer,
                pattern="^" + key.VOLUNTEER + "$",
            )
        ],
        state.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_name
            )
        ],
        state.ADDING_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_birthday
            )
        ],
        state.ADDING_CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_city
            )
        ],
        state.ADDING_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_phone
            )
        ],
        state.ADDING_EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_email
            )
        ],
        state.ADDING_MESSAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_message
            ),
            CommandHandler("skip", volunteer.skip_adding_message),
        ],
        state.SHOWING_VOLUNTEER: [edit_volunteer_conv],
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(key.END) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        key.END: state.SELECTING_ACTION,
        state.STOPPING: state.STOPPING,
    },
)
