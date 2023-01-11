from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import states
from bot.conversations import menu
from bot.conversations import volunteer_application as volunteer


edit_volunteer_conv = ConversationHandler(
    name="edit_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.select_volunteer_field,
            pattern="^" + str(states.EDIT_VOLUNTEER) + "$",
        ),
        CallbackQueryHandler(
            volunteer.send_email,
            pattern="^" + str(states.SEND_VOLUNTEER) + "$",
        ),
    ],
    states={
        states.VOLUNTEER_FEATURE: [
            CallbackQueryHandler(
                volunteer.ask_volunteer,
                pattern="^(?!" + str(states.END) + ").*$",
            ),
        ],
        states.TYPING_VOLUNTEER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.save_volunteer_input
            )
        ],
        states.VOLUNTEER_SENT: [
            CallbackQueryHandler(
                volunteer.end_editing, pattern="^" + str(states.END) + "$"
            ),
            CallbackQueryHandler(
                volunteer.end_sending, pattern="^" + str(states.SENT) + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            volunteer.end_editing, pattern="^" + str(states.END) + "$"
        ),
        CallbackQueryHandler(
            volunteer.end_sending, pattern="^" + str(states.SENT) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.END: states.SHOWING_VOLUNTEER,
        states.SENT: states.STOPPING,
        states.STOPPING: states.END,
    },
)

add_volunteer_conv = ConversationHandler(
    name="add_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.add_volunteer,
            pattern="^" + str(states.ADD_VOLUNTEER) + "$",
        )
    ],
    states={
        states.ADDING_VOLUNTEER: [
            CallbackQueryHandler(
                volunteer.adding_volunteer,
                pattern="^" + str(states.VOLUNTEER) + "$",
            )
        ],
        states.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_name
            )
        ],
        states.ADDING_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_birthday
            )
        ],
        states.ADDING_CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_city
            )
        ],
        states.ADDING_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_phone
            )
        ],
        states.ADDING_EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_email
            )
        ],
        states.ADDING_MESSAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_message
            ),
            CommandHandler("skip", volunteer.skip_adding_message),
        ],
        states.SHOWING_VOLUNTEER: [edit_volunteer_conv],
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
