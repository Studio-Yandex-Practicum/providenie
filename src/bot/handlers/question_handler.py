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
from bot.conversations import main_menu


edit_question_conv = ConversationHandler(
    name="edit_question_conv",
    entry_points=[
        CallbackQueryHandler(
            question.display_menu_editing_entered_value,
            pattern="^" + key.EDIT_QUESTION + "$",
        ),
        CallbackQueryHandler(
            question.send_message_to_curator,
            pattern="^" + key.SEND_QUESTION + "$",
        ),
    ],
    states={
        state.QUESTION_FEATURE: [
            CallbackQueryHandler(
                question.ask_new_value,
                pattern="^(?!" + str(key.END) + ").*$",
            ),
        ],
        state.TYPING_QUESTION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.save_new_value
            )
        ],
        state.QUESTION_SENT: [
            CallbackQueryHandler(
                main_menu.return_to_main_menu_after_sending_value,
                pattern="^" + key.SENT + "$",
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            question.display_all_new_entered_value,
            pattern="^" + str(key.END) + "$",
        ),
        CallbackQueryHandler(
            main_menu.return_to_main_menu_after_sending_value,
            pattern="^" + key.SENT + "$",
        ),
        CommandHandler("stop", main_menu.stop_nested),
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
            question.start_menu,
            pattern="^" + key.ASK_QUESTION + "$",
        )
    ],
    states={
        state.ASKING_QUESTION: [
            CallbackQueryHandler(
                question.ask_full_name,
                pattern="^" + key.QUESTION + "$",
            )
        ],
        state.ADDING_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.ask_question_theme
            )
        ],
        state.ADDING_THEME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.ask_question_message
            )
        ],
        state.ADDING_QUESTION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, question.save_question_message
            )
        ],
        state.SHOWING_QUESTION: [edit_question_conv],
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
