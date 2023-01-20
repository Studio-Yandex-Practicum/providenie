from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from bot.constans import fund_app_constans as constans
from bot import states
from ..conversations import fund_application as fund


# ВТОРОЙ УРОВЕНЬ Вступить в фонд
selection_handlers_second_level = [
    CallbackQueryHandler(
        fund.send_message_to_curator,
        pattern="^" + str(constans.CONFIRM_AND_SEND) + "$"
    ),
    CallbackQueryHandler(
        fund.change_data,
        pattern="^" + str(constans.CHANGE_DATA) + "$"
    ),
    CallbackQueryHandler(
        fund.end_second_menu,
        pattern="^" + str(constans.END_SECOND_LEVEL) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_mother,
        pattern="^" + str(constans.FIO_MOTHER) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_phone_mother,
        pattern="^" + str(constans.PHONE) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_email_mother,
        pattern="^" + str(constans.EMAIL) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_fio_child,
        pattern="^" + str(constans.FIO_CHILD) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_many_people_in_family,
        pattern="^" + str(constans.HOW_MANY_PEOPLE) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_city,
        pattern="^" + str(constans.CITY) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_address,
        pattern="^" + str(constans.ADDRESS) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_birthday,
        pattern="^" + str(constans.BIRTHDAY) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_place_birthday,
        pattern="^" + str(constans.PLACE_BIRTH) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_birth_date,
        pattern="^" + str(constans.BIRTH_DATE) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_weight,
        pattern="^" + str(constans.WEIGHT) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_height,
        pattern="^" + str(constans.HEIGHT) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_child_diagnosis,
        pattern="^" + str(constans.DIAGNOSIS) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_date_of_application,
        pattern="^" + str(constans.DATE_OF_APPLICATION) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_how_find_us,
        pattern="^" + str(constans.HOW_FOUND) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_city,
        pattern="^" + str(constans.CITY) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_which_fond_now,
        pattern="^" + str(constans.WHICH_FOND) + "$"
    ),
    CallbackQueryHandler(
        fund.asking_which_fonds_halped,
        pattern="^" + str(constans.WHICH_FOND_WAS_PREVIOUSLY) + "$"
    ),
]

dates_about_parent_and_child = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            fund.asking_fio_mother,
            pattern="^" + str(constans.JOIN_BUTTON) + "$"
        ),
        # MessageHandler(
        #     filters.TEXT & ~filters.COMMAND,
        #     fund.asking_fio_mother
        # )
    ],
    states={
        constans.RETURN_MOTHER_FIO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_fio_mother
            )
        ],
        constans.FIO_MOTHER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_phone_mother
            )
        ],
        constans.PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_email_mother
            )
        ],
        constans.EMAIL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_fio_child
            )
        ],
        constans.FIO_CHILD: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_how_many_people_in_family
            )
        ],
        constans.HOW_MANY_PEOPLE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_city
            )
        ],
        constans.CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_address
            )
        ],
        constans.ADDRESS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_birthday
            )
        ],
        constans.BIRTHDAY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_place_birthday
            )
        ],
        constans.PLACE_BIRTH: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_birth_date
            )
        ],
        constans.BIRTH_DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_weight
            )
        ],
        constans.WEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_height
            )
        ],
        constans.HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_child_diagnosis
            )
        ],
        constans.DIAGNOSIS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_date_of_application
            )
        ],
        constans.DATE_OF_APPLICATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_how_find_us
            )
        ],
        constans.HOW_FOUND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_which_fond_now
            )
        ],
        constans.WHICH_FOND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.asking_which_fonds_halped
            )
        ],
        constans.WHICH_FOND_WAS_PREVIOUSLY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.show_user_information
            )
        ],
        constans.SHOW_INFORMATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.send_or_change_data
            )
        ],
        constans.SHOW_EDIT_INFORMATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fund.show_user_edit_information
            )
        ],
        # constans.SEND_CHANGE_END: selection_handlers_second_level,
        # constans.BAD_ANSWER_SECOND_LEVEL: selection_handlers_second_level,
        constans.EDIT_USER_DATА: selection_handlers_second_level,
    },

    fallbacks=[CommandHandler("stop", fund.stop_nested)],

    # Возврат на первый уровень
    map_to_parent={
        constans.END_FIRST_LEVEL: constans.JOIN_PROGRAM,
        # constans.MESSAGE_SENT_SUCCESSFULLY: constans.JOIN_TO_PROGRAMM,
        # constans.QUESTION_THIRD_MENU: constans.JOIN_TO_PROGRAMM,
        # constans.BAD_FIO_MOTHER: constans.BAD_VALUES,
        # constans.BAD_FIO_MOTHER: constans.JOIN_TO_PROGRAMM,
        # constans.RETURN_MOTHER_FIO: constans.GO_SECOND_LEVEL,
        states.STOPPING: states.STOPPING
    },
)


# ПЕРВЫЙ УРОВЕНЬ Вступить в фонд
selection_handlers = [
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(constans.LOOK_WORLD_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(constans.REABILITATION_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(constans.PSIHO_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(constans.KIND_LESSONS_PROGRAM) + "$"
    ),
    CallbackQueryHandler(
        fund.join_or_not_to_program,
        pattern="^" + str(constans.SAY_YES) + "$"
    ),
    dates_about_parent_and_child,
    # CallbackQueryHandler(
    #     fund.go_second_level,
    #     pattern="^" + str(constans.JOIN_BUTTON) + "$"
    # ),
    CallbackQueryHandler(
        fund.return_main_menu,
        pattern="^" + str(constans.MAIN_MENU) + "$"
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
        # constans.CHOICE_PROGRAMM: selection_handlers,
        constans.JOIN_PROGRAM: selection_handlers,
        # constans.BAD_VALUES: selection_handlers,
        constans.GO_SECOND_LEVEL: [dates_about_parent_and_child]
    },

    fallbacks=[CommandHandler("stop", fund.stop_nested)],

    map_to_parent={
        constans.END_MAIN_MENU: states.SELECTING_ACTION,
        states.STOPPING: states.STOPPING,
    },
)