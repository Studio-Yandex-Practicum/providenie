from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from bot.constans import fund_app_callbacks as fund_callbacks
from bot.constans import fund_app_states as fund_states
from bot import states
from ..conversations import fund_application as fund


# ВТОРОЙ УРОВЕНЬ Вступить в фонд
selection_handlers_second_level = [
    CallbackQueryHandler(
        fund.send_message_to_curator,
        pattern="^" + str(fund_callbacks.CONFIRM_AND_SEND) + "$"
    ),
    CallbackQueryHandler(
        fund.change_data,
        pattern="^" + str(fund_callbacks.CHANGE_DATA) + "$"
    ),
    CallbackQueryHandler(
        fund.end_second_menu,
        pattern="^" + str(fund_callbacks.END_SECOND_LEVEL) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_mother,
        pattern="^" + str(fund_callbacks.EDIT_FIO_MOTHER) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_phone_mother,
        pattern="^" + str(fund_callbacks.EDIT_PHONE) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_email_mother,
        pattern="^" + str(fund_callbacks.EDIT_EMAIL) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_child,
        pattern="^" + str(fund_callbacks.EDIT_FIO_CHILD) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_many_people_in_family,
        pattern="^" + str(fund_callbacks.EDIT_HOW_MANY_PEOPLE) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_city,
        pattern="^" + str(fund_callbacks.EDIT_CITY) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_address,
        pattern="^" + str(fund_callbacks.EDIT_ADDRESS) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_birthday,
        pattern="^" + str(fund_callbacks.EDIT_BIRTHDAY) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_place_birthday,
        pattern="^" + str(fund_callbacks.EDIT_PLACE_BIRTH) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_birth_date,
        pattern="^" + str(fund_callbacks.EDIT_BIRTH_DATE) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_weight,
        pattern="^" + str(fund_callbacks.EDIT_WEIGHT) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_height,
        pattern="^" + str(fund_callbacks.EDIT_HEIGHT) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_diagnosis,
        pattern="^" + str(fund_callbacks.EDIT_DIAGNOSIS) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_find_us,
        pattern="^" + str(fund_callbacks.EDIT_HOW_FOUND) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_city,
        pattern="^" + str(fund_callbacks.EDIT_CITY) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_which_fond_now,
        pattern="^" + str(fund_callbacks.EDIT_WHICH_FOND) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_which_fonds_halped,
        pattern="^" + str(fund_callbacks.EDIT_WHICH_FOND_WAS_PREVIOUSLY) + "$"
    ),
]

dates_about_parent_and_child = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            fund.asking_fio_mother,
            pattern="^" + str(fund_callbacks.JOIN_BUTTON) + "$"
        ),
    ],
    states={
        fund_states.RETURN_MOTHER_FIO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_fio_mother
            )
        ],
        fund_states.FIO_MOTHER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_phone_mother
            )
        ],
        fund_states.PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_email_mother
            )
        ],
        fund_states.EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_fio_child
            )
        ],
        fund_states.FIO_CHILD: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_how_many_people_in_family
            )
        ],
        fund_states.HOW_MANY_PEOPLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_city
            )
        ],
        fund_states.CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_address
            )
        ],
        fund_states.ADDRESS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_birthday
            )
        ],
        fund_states.BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_place_birthday
            )
        ],
        fund_states.PLACE_BIRTH: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_birth_date
            )
        ],
        fund_states.BIRTH_DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_weight
            )
        ],
        fund_states.WEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_height
            )
        ],
        fund_states.HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_diagnosis
            )
        ],
        fund_states.DIAGNOSIS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_date_of_application
            )
        ],
        fund_states.HOW_FOUND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_which_fond_now
            )
        ],
        fund_states.WHICH_FOND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_which_fonds_halped
            )
        ],
        fund_states.WHICH_FOND_WAS_PREVIOUSLY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.show_user_information
            )
        ],
        fund_states.EDIT_USER_DATА: selection_handlers_second_level,
    },

    fallbacks=[CommandHandler("stop", fund.stop_nested)],

    # Возврат на первый уровень
    map_to_parent={
        fund_states.END_FIRST_LEVEL: fund_states.JOIN_PROGRAM,
        states.STOPPING: states.STOPPING
    },
)


# ПЕРВЫЙ УРОВЕНЬ Вступить в фонд
selection_handlers = [
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(fund_callbacks.LOOK_WORLD_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(fund_callbacks.REABILITATION_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(fund_callbacks.PSIHO_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(fund_callbacks.KIND_LESSONS_PROGRAM) + "$"
    ),
    dates_about_parent_and_child,
    CallbackQueryHandler(
        fund.return_main_menu,
        pattern="^" + str(fund_callbacks.MAIN_MENU) + "$"
    ),
    CallbackQueryHandler(
        fund.end,
        pattern="^" + str(fund.END) + "$"
    ),
]


conv_handler_join_to_fond = ConversationHandler(
    name="conv_handler_join_to_fond",
    entry_points=[
        CallbackQueryHandler(
            fund.application_to_the_fond,
            pattern="^" + str(states.REQUEST) + "$"
        ),
    ],
    states={
        fund_states.JOIN_PROGRAM: selection_handlers,
        fund_states.GO_SECOND_LEVEL: [dates_about_parent_and_child]
    },

    fallbacks=[CommandHandler("stop", fund.stop_nested)],

    map_to_parent={
        fund_states.END_MAIN_MENU: states.SELECTING_ACTION,
        states.STOPPING: states.STOPPING,
    },
)
