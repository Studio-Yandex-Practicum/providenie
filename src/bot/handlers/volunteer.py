from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import constants as const
from bot.conversations import menu
from bot.conversations import volunteer_application as volunteer


edit_volunteer_conv = ConversationHandler(
    name="edit_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.select_volunteer_field,
            pattern="^" + str(const.EDIT_VOLUNTEER) + "$",
        ),
        CallbackQueryHandler(
            volunteer.send_email, pattern="^" + str(const.SEND_VOLUNTEER) + "$"
        ),
    ],
    states={
        const.VOLUNTEER_FEATURE: [
            CallbackQueryHandler(
                volunteer.ask_volunteer,
                pattern="^(?!" + str(const.END) + ").*$",
            ),
        ],
        const.TYPING_VOLUNTEER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.save_volunteer_input
            )
        ],
        const.VOLUNTEER_SENT: [
            CallbackQueryHandler(
                volunteer.end_editing, pattern="^" + str(const.END) + "$"
            ),
            CallbackQueryHandler(
                volunteer.end_sending, pattern="^" + str(const.SENT) + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            volunteer.end_editing, pattern="^" + str(const.END) + "$"
        ),
        CallbackQueryHandler(
            volunteer.end_sending, pattern="^" + str(const.SENT) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        const.END: const.SHOWING_VOLUNTEER,
        const.SENT: const.STOPPING,
        const.STOPPING: const.END,
    },
)

add_volunteer_conv = ConversationHandler(
    name="add_volunteer_conv",
    entry_points=[
        CallbackQueryHandler(
            volunteer.add_volunteer,
            pattern="^" + str(const.ADD_VOLUNTEER) + "$",
        )
    ],
    states={
        const.ADDING_VOLUNTEER: [
            CallbackQueryHandler(
                volunteer.adding_volunteer,
                pattern="^" + str(const.VOLUNTEER) + "$",
            )
        ],
        const.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_name
            )
        ],
        const.ADDING_BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_birthday
            )
        ],
        const.ADDING_CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_city
            )
        ],
        const.ADDING_PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_phone
            )
        ],
        const.ADDING_EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_email
            )
        ],
        const.ADDING_MESSAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, volunteer.adding_message
            ),
            CommandHandler("skip", volunteer.skip_adding_message),
        ],
        const.SHOWING_VOLUNTEER: [edit_volunteer_conv],
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(const.END) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        const.END: const.SELECTING_ACTION,
        const.STOPPING: const.STOPPING,
    },
)
