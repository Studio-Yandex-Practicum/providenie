from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import keys as key
from bot import states as state
from bot.conversations import ask_question as question
from bot.conversations import menu


edit_question_conv = ConversationHandler(
    name="edit_question_conv",
    entry_points=[
        CallbackQueryHandler(
            question.select_question_field,
            pattern="^" + str(key.EDIT_QUESTION) + "$",
        ),
        CallbackQueryHandler(
            question.send_question,
            pattern="^" + str(key.SEND_QUESTION) + "$",
        ),
    ],
    states={
        state.QUESTION_FEATURE: [
            CallbackQueryHandler(
                question.ask_data,
                pattern="^(?!" + str(key.END) + ").*$",
            ),
        ],
        state.TYPING_QUESTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, question.save_data)
        ],
        state.QUESTION_SENT: [
            CallbackQueryHandler(
                menu.end_sending, pattern="^" + str(key.SENT) + "$"
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            question.end_editing, pattern="^" + str(key.END) + "$"
        ),
        CallbackQueryHandler(
            menu.end_sending, pattern="^" + str(key.SENT) + "$"
        ),
        CommandHandler("stop", menu.stop_nested),
    ],
    map_to_parent={
        key.END: state.SHOWING_QUESTION,
        key.SENT: state.STOPPING,
        state.STOPPING: key.END,
    },
)

ask_question_conv = ConversationHandler(
    name="ask_question_conv",
    entry_points=[
        CallbackQueryHandler(
            question.ask_question,
            pattern="^" + str(key.ASK_QUESTION) + "$",
        )
    ],
    states={
        state.ASKING_QUESTION: [
            CallbackQueryHandler(
                question.asking_question,
                pattern="^" + str(key.QUESTION) + "$",
            )
        ],
        state.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.adding_name
            )
        ],
        state.ADDING_THEME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.adding_theme
            )
        ],
        state.ADDING_QUESTION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.adding_question
            )
        ],
        state.SHOWING_QUESTION: [edit_question_conv],
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
