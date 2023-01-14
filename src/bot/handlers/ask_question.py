from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import states
from bot.conversations import menu
from bot.conversations import ask_question as question


edit_question_conv = ConversationHandler(
    name="edit_question_conv",
    entry_points=[
        CallbackQueryHandler(
            question.select_question_field,
            pattern="^" + str(states.EDIT_QUESTION) + "$",
        ),
        CallbackQueryHandler(
            question.send_question,
            pattern="^" + str(states.SEND_QUESTION) + "$",
        ),
    ],
    states={
        states.QUESTION_FEATURE: [
            CallbackQueryHandler(
                question.ask_data,
                pattern="^(?!" + str(states.END) + ").*$",
            ),
        ],
        states.TYPING_QUESTION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.save_data
            )
        ],
        # states.VOLUNTEER_SENT: [
        #     CallbackQueryHandler(
        #         volunteer.end_editing, pattern="^" + str(states.END) + "$"
        #     ),
        #     CallbackQueryHandler(
        #         volunteer.end_sending, pattern="^" + str(states.SENT) + "$"
        #     ),
        # ],
    },
    fallbacks=[
        CallbackQueryHandler(
            question.end_editing, pattern="^" + str(states.END) + "$"
        ),
        CallbackQueryHandler(
            menu.end_sending, pattern="^" + str(states.SENT) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        states.END: states.SHOWING_QUESTION,
        states.SENT: states.STOPPING,
        states.STOPPING: states.END,
    },
)

ask_question_conv = ConversationHandler(
    name="ask_question_conv",
    entry_points=[
        CallbackQueryHandler(
            question.ask_question,
            pattern="^" + str(states.ASK_QUESTION) + "$",
        )
    ],
    states={
        states.ASKING_QUESTION: [
            CallbackQueryHandler(
                question.asking_question,
                pattern="^" + str(states.QUESTION) + "$",
            )
        ],
        states.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.adding_name
            )
        ],
        states.ADDING_THEME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.adding_theme
            )
        ],
        states.ADDING_QUESTION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.adding_question
            )
        ],
        states.SHOWING_QUESTION: [edit_question_conv],
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
