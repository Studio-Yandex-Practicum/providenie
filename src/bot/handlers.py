# Не знаю будет ли работать, раскидав функции отдельно от хендлеров

from telegram.ext import (
    CallbackQueryHandler, CommandHandler,
    ConversationHandler, MessageHandler, filters)

# Импорт констант для маршрутов
from conversations.fund_application import (
    LOOK_WORLD_PROGRAMM, REABILITATION_PROGRAMM, PSIHO_PROGRAMM,
    KIND_ARMS_PROGRAMM, FIO_MOTHER, PHONE, EMAIL, FIO_CHILD,
    HOW_MANY_PEOPLES, CITY, ADRESS, DATE_BIRTH,
    SPACING, WEIGHT, HEIGHT, DIAGNOZES, DATE_OF_APPLICATION,
    HOW_FIND_US, WHICH_FOND, WHICH_FOND_WAS_PREVIOUSLY,
    CHOISE_PROGRAMM, JOIN_TO_PROGRAMM, JOIN_BUTTON, BAD_ANSWER_SECOND_LEVEL,
    SHOW_INFORMATION, CONFIRM_AND_SEND, END_SECOND_LEVEL, SEND_CHANGE_END,
    CHANGE_DATES, MESSAGE_SENT_SUCCESSFULLY, END_FIRST_LEVEL,
    SHOW_EDIT_INFORMATIONS, SAY_YES, QUESTION_THIRD_MENU, BAD_FIO_MOTHER,
    BAD_VALUES, RETURN_MOTHER_FIO, GO_SECOND_LEVEL, EDIT_USER_DATES,
    PLACE_BIRTH, END
)

# Импорт подпрограмм функции вступления в фонд
from conversations.fund_application import (
    send_message_to_curator, change_dates, end_second_menu,
    asking_fio_mother, asking_phone_mother, asking_email_mother,
    asking_fio_child, asking_how_many_people_in_famaly,
    asking_city, asking_adress, asking_child_birthday,
    asking_place_birthday, asking_spacing, asking_child_weight,
    asking_child_height, asking_child_diagnozes,
    asking_date_of_application, asking_how_find_us,
    asking_which_fond_now, asking_which_fonds_halped,
    show_user_information, send_or_change_dates,
    show_user_edit_information, stop, join_or_not_to_programm,
    go_second_level, end
)






# ВТОРОЙ УРОВЕНЬ Вступить в фонд
selection_handlers_second_level = [
        CallbackQueryHandler(send_message_to_curator, pattern="^" + str(CONFIRM_AND_SEND) + "$"),
        CallbackQueryHandler(change_dates, pattern="^" + str(CHANGE_DATES) + "$"),
        CallbackQueryHandler(end_second_menu, pattern="^" + str(END_SECOND_LEVEL) + "$"),
        CallbackQueryHandler(asking_fio_mother, pattern="^" + str(FIO_MOTHER) + "$"),
        CallbackQueryHandler(asking_phone_mother, pattern="^" + str(PHONE) + "$"),
        CallbackQueryHandler(asking_email_mother, pattern="^" + str(EMAIL) + "$"),
        CallbackQueryHandler(asking_fio_child, pattern="^" + str(FIO_CHILD) + "$"),
        CallbackQueryHandler(asking_how_many_people_in_famaly, pattern="^" + str(HOW_MANY_PEOPLES) + "$"),
        CallbackQueryHandler(asking_city, pattern="^" + str(CITY) + "$"),
        CallbackQueryHandler(asking_adress, pattern="^" + str(ADRESS) + "$"),
        CallbackQueryHandler(asking_child_birthday, pattern="^" + str(DATE_BIRTH) + "$"),
        CallbackQueryHandler(asking_place_birthday, pattern="^" + str(PLACE_BIRTH) + "$"),
        CallbackQueryHandler(asking_spacing, pattern="^" + str(SPACING) + "$"),
        CallbackQueryHandler(asking_child_weight, pattern="^" + str(WEIGHT) + "$"),
        CallbackQueryHandler(asking_child_height, pattern="^" + str(HEIGHT) + "$"),
        CallbackQueryHandler(asking_child_diagnozes, pattern="^" + str(DIAGNOZES) + "$"),
        CallbackQueryHandler(asking_date_of_application, pattern="^" + str(DATE_OF_APPLICATION) + "$"),
        CallbackQueryHandler(asking_how_find_us, pattern="^" + str(HOW_FIND_US) + "$"),
        CallbackQueryHandler(asking_city, pattern="^" + str(CITY) + "$"),
        CallbackQueryHandler(asking_which_fond_now, pattern="^" + str(WHICH_FOND) + "$"),
        CallbackQueryHandler(asking_which_fonds_halped, pattern="^" + str(WHICH_FOND_WAS_PREVIOUSLY) + "$"),
    ]

dates_about_parent_and_child = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, asking_fio_mother)],
    states={
        FIO_MOTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_phone_mother)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_email_mother)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_fio_child)],
        FIO_CHILD: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_how_many_people_in_famaly)],
        HOW_MANY_PEOPLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_city)],
        CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_adress)],
        ADRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_child_birthday)],
        DATE_BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_place_birthday)],
        PLACE_BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_spacing)],
        SPACING: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_child_weight)],
        WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_child_height)],
        HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_child_diagnozes)],
        DIAGNOZES: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_date_of_application)],
        DATE_OF_APPLICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_how_find_us)],
        HOW_FIND_US: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_which_fond_now)],
        WHICH_FOND: [MessageHandler(filters.TEXT & ~filters.COMMAND, asking_which_fonds_halped)],
        WHICH_FOND_WAS_PREVIOUSLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_user_information)],
        SHOW_INFORMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_or_change_dates)],
        SHOW_EDIT_INFORMATIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_user_edit_information)],
        SEND_CHANGE_END: selection_handlers_second_level,
        BAD_ANSWER_SECOND_LEVEL: selection_handlers_second_level,
        EDIT_USER_DATES: selection_handlers_second_level,
        },

    fallbacks=[CommandHandler("stop", stop)],

    # Возврат на первый уровень
    map_to_parent={
        END_FIRST_LEVEL: JOIN_TO_PROGRAMM,
        MESSAGE_SENT_SUCCESSFULLY: CHOISE_PROGRAMM,
        QUESTION_THIRD_MENU: CHOISE_PROGRAMM,
        BAD_FIO_MOTHER: BAD_VALUES,
        RETURN_MOTHER_FIO: GO_SECOND_LEVEL,
    },
)


# ПЕРВЫЙ УРОВЕНЬ Вступить в фонд
selection_handlers = [
    CallbackQueryHandler(join_or_not_to_programm, pattern="^" + str(LOOK_WORLD_PROGRAMM) + "$"),
    CallbackQueryHandler(join_or_not_to_programm, pattern="^" + str(REABILITATION_PROGRAMM) + "$"),
    CallbackQueryHandler(join_or_not_to_programm, pattern="^" + str(PSIHO_PROGRAMM) + "$"),
    CallbackQueryHandler(join_or_not_to_programm, pattern="^" + str(KIND_ARMS_PROGRAMM) + "$"),
    CallbackQueryHandler(join_or_not_to_programm, pattern="^" + str(SAY_YES) + "$"),
    CallbackQueryHandler(go_second_level, pattern="^" + str(JOIN_BUTTON) + "$"),
    CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
]


# Здесь должна принимаиться CallbackQueryHandler и КОНСТАНТА из ОСНОВНОГО МЕНЮ
conv_handler = ConversationHandler(
    # entry_points=[CommandHandler("start", application_to_the_fond)],
    states={
        CHOISE_PROGRAMM: selection_handlers,
        JOIN_TO_PROGRAMM: selection_handlers,
        BAD_VALUES: selection_handlers,
        GO_SECOND_LEVEL: [dates_about_parent_and_child]
    },

    # Здесь должна быть функция общая для всех этапов Робота
    fallbacks=[CommandHandler("stop", stop)],
)
