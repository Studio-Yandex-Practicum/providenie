from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from bot.constans import fund_app_callbacks as fund_callbacks
from bot.constans import fund_app_states as fund_states
from bot import keys, states
from ..conversations import fund_application as fund


# ВТОРОЙ УРОВЕНЬ Вступить в фонд
selection_handlers_second_level = [
    CallbackQueryHandler(
        fund.send_message_to_curator,
        pattern="^" + fund_callbacks.CONFIRM_AND_SEND + "$"
    ),
    CallbackQueryHandler(
        fund.change_data,
        pattern="^" + fund_callbacks.CHANGE_DATA + "$"
    ),
    CallbackQueryHandler(
        fund.end_second_menu,
        pattern="^" + fund_callbacks.END_SECOND_LEVEL + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_mother,
        pattern="^" + fund_callbacks.FIO_MOTHER + "$"
    ),
    CallbackQueryHandler(
        fund.asking_phone_mother,
        pattern="^" + fund_callbacks.PHONE + "$"
    ),
    CallbackQueryHandler(
        fund.asking_email_mother,
        pattern="^" + fund_callbacks.EMAIL + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_child,
        pattern="^" + fund_callbacks.FIO_CHILD + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_many_people_in_family,
        pattern="^" + fund_callbacks.HOW_MANY_PEOPLE + "$"
    ),
    CallbackQueryHandler(
        fund.asking_city,
        pattern="^" + fund_callbacks.CITY + "$"
    ),
    CallbackQueryHandler(
        fund.asking_address,
        pattern="^" + fund_callbacks.ADDRESS + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_birthday,
        pattern="^" + fund_callbacks.BIRTHDAY + "$"
    ),
    CallbackQueryHandler(
        fund.asking_place_birthday,
        pattern="^" + fund_callbacks.PLACE_BIRTH + "$"
    ),
    CallbackQueryHandler(
        fund.asking_birth_date,
        pattern="^" + fund_callbacks.BIRTH_DATE + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_weight,
        pattern="^" + fund_callbacks.WEIGHT + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_height,
        pattern="^" + fund_callbacks.HEIGHT + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_diagnosis,
        pattern="^" + fund_callbacks.DIAGNOSIS + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_found_us,
        pattern="^" + fund_callbacks.HOW_FOUND + "$"
    ),
    CallbackQueryHandler(
        fund.asking_city,
        pattern="^" + fund_callbacks.CITY + "$"
    ),
    CallbackQueryHandler(
        fund.asking_which_fund_now,
        pattern="^" + fund_callbacks.WHICH_FUND + "$"
    ),
    CallbackQueryHandler(
        fund.asking_which_funds_helped,
        pattern="^" + fund_callbacks.WHICH_FUND_WAS_PREVIOUSLY + "$"
    ),
]

dates_about_parent_and_child = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            fund.asking_fio_mother,
            pattern="^" + fund_callbacks.JOIN_BUTTON + "$"
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
                fund.asking_which_fund_now
            )
        ],
        fund_states.WHICH_FUND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_which_funds_helped
            )
        ],
        fund_states.WHICH_FUND_WAS_PREVIOUSLY: [
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
        pattern="^" + fund_callbacks.LOOK_WORLD_PROGRAM + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + fund_callbacks.REABILITATION_PROGRAM + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + fund_callbacks.PSIHO_PROGRAM + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + fund_callbacks.KIND_LESSONS_PROGRAM + "$"
    ),
    dates_about_parent_and_child,
    CallbackQueryHandler(
        fund.return_main_menu,
        pattern="^" + fund_callbacks.MAIN_MENU + "$"
    ),
    CallbackQueryHandler(
        fund.end,
        pattern="^" + str(fund.END) + "$"
    ),
]


conv_handler_join_to_fund = ConversationHandler(
    name="conv_handler_join_to_fund",
    entry_points=[
        CallbackQueryHandler(
            fund.application_to_the_fund,
            pattern="^" + str(keys.REQUEST) + "$"
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
