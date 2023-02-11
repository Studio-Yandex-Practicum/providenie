from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from ..conversations import fund_application as fund
from bot import keys, states


# ВТОРОЙ УРОВЕНЬ Вступить в фонд
selection_handlers_second_level = [
    CallbackQueryHandler(
        fund.send_message_to_curator,
        pattern="^" + keys.CONFIRM_AND_SEND + "$",
    ),
    CallbackQueryHandler(
        fund.change_data, pattern="^" + keys.CHANGE_DATA + "$"
    ),
    CallbackQueryHandler(
        fund.end_second_menu,
        pattern="^" + keys.END_SECOND_LEVEL + "$",
    ),
    CallbackQueryHandler(
        fund.asking_fio_mother, pattern="^" + keys.FIO_MOTHER + "$"
    ),
    CallbackQueryHandler(
        fund.asking_phone_mother, pattern="^" + keys.PHONE + "$"
    ),
    CallbackQueryHandler(
        fund.asking_email_mother, pattern="^" + keys.EMAIL + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_child, pattern="^" + keys.FIO_CHILD + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_many_people_in_family,
        pattern="^" + keys.HOW_MANY_PEOPLE + "$",
    ),
    CallbackQueryHandler(fund.asking_city, pattern="^" + keys.CITY + "$"),
    CallbackQueryHandler(
        fund.asking_address, pattern="^" + keys.ADDRESS + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_birthday, pattern="^" + keys.BIRTHDAY + "$"
    ),
    CallbackQueryHandler(
        fund.asking_place_birthday,
        pattern="^" + keys.PLACE_BIRTH + "$",
    ),
    CallbackQueryHandler(
        fund.asking_birth_date, pattern="^" + keys.BIRTH_DATE + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_weight, pattern="^" + keys.WEIGHT + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_height, pattern="^" + keys.HEIGHT + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_diagnosis,
        pattern="^" + keys.DIAGNOSIS + "$",
    ),
    CallbackQueryHandler(
        fund.asking_how_found_us, pattern="^" + keys.HOW_FOUND + "$"
    ),
    CallbackQueryHandler(fund.asking_city, pattern="^" + keys.CITY + "$"),
    CallbackQueryHandler(
        fund.asking_which_fund_now,
        pattern="^" + keys.WHICH_FUND + "$",
    ),
    CallbackQueryHandler(
        fund.asking_which_funds_helped,
        pattern="^" + keys.WHICH_FUND_WAS_PREVIOUSLY + "$",
    ),
]

dates_about_parent_and_child = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            fund.asking_fio_mother,
            pattern="^" + keys.JOIN_BUTTON + "$",
        ),
    ],
    states={
        states.RETURN_MOTHER_FIO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_fio_mother
            )
        ],
        states.FIO_MOTHER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_phone_mother
            )
        ],
        states.PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_email_mother
            )
        ],
        states.EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_fio_child
            )
        ],
        states.FIO_CHILD: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_how_many_people_in_family,
            )
        ],
        states.HOW_MANY_PEOPLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, fund.asking_city)
        ],
        states.CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_address
            )
        ],
        states.ADDRESS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_child_birthday
            )
        ],
        states.BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_place_birthday
            )
        ],
        states.PLACE_BIRTH: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_birth_date
            )
        ],
        states.BIRTH_DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_child_weight
            )
        ],
        states.WEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_child_height
            )
        ],
        states.HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_child_diagnosis
            )
        ],
        states.DIAGNOSIS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_how_found_us
            )
        ],
        states.HOW_FOUND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_which_fund_now
            )
        ],
        states.WHICH_FUND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.asking_which_funds_helped
            )
        ],
        states.WHICH_FUND_WAS_PREVIOUSLY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, fund.show_user_information
            )
        ],
        states.EDIT_USER_DATА: selection_handlers_second_level,
    },
    fallbacks=[CommandHandler("stop", fund.stop_nested)],
    # Возврат на первый уровень
    map_to_parent={
        states.END_FIRST_LEVEL: states.JOIN_PROGRAM,
        states.STOPPING: states.STOPPING,
    },
)


# ПЕРВЫЙ УРОВЕНЬ Вступить в фонд
selection_handlers = [
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + keys.LOOK_WORLD_PROGRAM + "$",
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + keys.REABILITATION_PROGRAM + "$",
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + keys.PSIHO_PROGRAM + "$",
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + keys.KIND_LESSONS_PROGRAM + "$",
    ),
    dates_about_parent_and_child,
    CallbackQueryHandler(
        fund.return_main_menu, pattern="^" + keys.MAIN_MENU + "$"
    ),
    CallbackQueryHandler(fund.end, pattern="^" + str(fund.END) + "$"),
]


conv_handler_join_to_fund = ConversationHandler(
    name="conv_handler_join_to_fund",
    entry_points=[
        CallbackQueryHandler(
            fund.application_to_the_fund, pattern="^" + str(keys.REQUEST) + "$"
        ),
    ],
    states={
        states.JOIN_PROGRAM: selection_handlers,
        states.GO_SECOND_LEVEL: [dates_about_parent_and_child],
    },
    fallbacks=[CommandHandler("stop", fund.stop_nested)],
    map_to_parent={
        states.END_MAIN_MENU: states.SELECTING_ACTION,
        states.STOPPING: states.STOPPING,
    },
)
