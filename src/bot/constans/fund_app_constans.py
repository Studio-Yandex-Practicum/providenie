# Константы этапов разговора
from telegram import ReplyKeyboardMarkup


(
    LOOK_WORLD_PROGRAM, REABILITATION_PROGRAM,
    PSIHO_PROGRAM, KIND_LESSONS_PROGRAM
) = range(4)

(
    FIO_MOTHER,
    PHONE,
    EMAIL,
    FIO_CHILD,
    HOW_MANY_PEOPLE,
    CITY,
    ADDRESS,
    BIRTHDAY,
    LOCAL_OF_BIRTH,
    BIRTH_DATE,
    WEIGHT,
    HEIGHT,
    DIAGNOSIS,
    DATE_OF_APPLICATION,
    HOW_FOUND,
    WHICH_FOND,
    WHICH_FOND_WAS_PREVIOUSLY,
    START_OVER,
) = range(4, 22)


CHOICE_PROGRAM, JOIN_PROGRAM = range(22, 24)
(
    JOIN_BUTTON,
    BAD_ANSWER_SECOND_LEVEL,
    SHOW_INFORMATION,
    CONFIRM_AND_SEND,
    END_SECOND_LEVEL,
    SEND_CHANGE_END,
    CHANGE_DATA,
    MESSAGE_SENT_SUCCESSFULLY,
    END_FIRST_LEVEL,
    EDIT_MODE,
    SHOW_EDIT_INFORMATION,
    SAY_YES,
    SAY_NO,
    QUESTION_THIRD_MENU,
    BAD_FIO_MOTHER,
    BAD_VALUES,
    RETURN_MOTHER_FIO,
    GO_SECOND_LEVEL,
) = range(24, 42)

EDIT_PHONE, EDIT_USER_DATА, PLACE_BIRTH = range(42, 45)

(
    START_JOIN_TO_FOND,
    END_MAIN_MENU,
    RETURN_FROM_JOIN_TO_FOND,
    GO_MAIN_MENU,
    MAIN_MENU,
    GO_TO_JOIN_FOND,
    START_QUATIONS,
) = range(45, 52)


# Различные ответы, вопросы, описание и документы
ANSWERS_DICT = {
    "bad_answer": """
        Неопределено, всё исправится куратором чуть позже.
    """,
    "bad_fio_mother": """
        Неверно введено ФИО, пожалуйста, нажмите исправить.
    """,
    "bad_phone_number": """
        Неверно введён номер телефона, пожалуйста, нажмите исправить.
    """,
    "bad_email": """
        Неверно введён email, пожалуйста, нажмите исправить.
    """,
    "bad_child_fio": """
        Неверно введено ФИО ребёнка, пожалуйста, нажмите исправить.
    """,
    "bad_people_in_famaly": """
        Неверно введено количество членов семьи,
        пожалуйста, нажмите исправить.
    """,
    "bad_city": """
        Неверно введено название города, пожалуйста, нажмите исправить.
    """,
    "bad_address": """
        Неверно введён адрес, пожалуйста, нажмите исправить.
    """,
    "bad_birthday": """
        Неверно введена дата рождения ребёнка, пожалуйста, нажмите исправить.
    """,
    "bad_place_birth": """
        Неверно введено место рождения ребёнка, пожалуйста, нажмите исправить.
    """,
    "bad_birth_date": """
        Неверно введён срок рождения ребёнка,
        пожалуйста, нажмите исправить.
    """,
    "bad_weight": """
        Неверно введён вес ребёнка, пожалуйста, нажмите исправить.
    """,
    "bad_height": """
        Неверно введён рост ребёнка, пожалуйста, нажмите исправить.
    """,
    "bad_diagnosis": """
        Неверно введён диагноз ребёнка, пожалуйста, нажмите исправить.
    """,
    "bad_date_application": """
        Неверно введена дата обращения, пожалуйста, нажмите исправить.
    """,
}

QUESTIONS_DICT = {
    "fio_mother": "Введите ФИО мамы.",
    "phone_number": "Введите телефон.",
    "email": "Введите ваш email.",
    "fio_child": "Введите ФИО ребёнка.",
    "how_many_people": "Введите количество членов семьи. (числом)",
    "city": "Введите город проживания.",
    "address": "Введите адрес проживания.",
    "birthday": "Введите дату рождения ребёнка. (ДД.ММ.ГГГГ)",
    "place_birth": "Введите место рождения ребёнка.",
    "bad_birth_date": "Введите срок на котором родился ребёнок. (Неделя, числом)",
    "weight": "Введите вес ребёнка. (Числом)",
    "height": "Введите рост ребёнка. (Числом)",
    "diagnosis": """
        Введите диагнозы ребёнка.
        (Через запятую, при наличии нескольких)""",
    "date_aplication": "Введите дату обращения в Фонд. (ДД.ММ.ГГГГ)",
    "how_find_fond": "Откуда вы узнали о нашем фонде?",
    "which_fond": "Вам помогали фонды раньше? Если да, то какие?",
    "fond_now": """Состоите ли вы в данный момент в каком-либо фонде,
        если да, то напишите название фонда?""",
}

BUTTONS_TEXT = {
    "fio_mother": "ФИО мамы.",
    "phone_number": "Телефон.",
    "email": "Email.",
    "fio_child": "ФИО ребёнка.",
    "how_many_people": "Количество членов семьи",
    "city": "Город",
    "address": "Адрес",
    "birthday": "Дата рождения ребёнка",
    "place_birth": "Место рождения ребёнка",
    "birth_date": "Срок рождения",
    "weight": "Вес",
    "height": "Рост",
    "diagnosis": "Диагнозы",
    "date_aplication": "Дата обращения",
    "how_find_fond": "Как узнали о нас",
    "which_fond": "В каком фонде сейчас",
    "fond_now": "Какие фонды помогали",
    "resume": "Продолжить",
    "confirm_and_send": "Подтвердить и отправить",
    "change_data": "Изменить данные",
    "back": "Назад",
    "back_to_menu": "Назад в меню",
    "join": "Вступить",
    "main_menu": "Главное меню",
}


MESSAGE_SUCCESSFUL_DEPARTURE_TO_CURATOR = """
    Ваши данные успешно отправлены куратору.
    Ожидайте сообщения от куратора.
    Так же нужно будет подготовить документы:\n
"""


REQUIRED_DOCUMENTS = """
Необходимые документы:\n
- Справка о многодетности, малообеспеченности, инвалидности (фото).\n
- Справка 2 НДФЛ родителей или любая форма справки,
    подтверждающая ДОХОД РОДИТЕЛЕЙ\n
- Выписка с рекомендациями (фото/скан)\n
- Свидетельство о рождении (фото/скан)\n
- Паспорт (фото/скан)\n
- Счёт на лечение (какое лечение требуется, стоимость)
    или ссылка на то, что необходимо приобрести\n
"""


LOOK_AT_WORLD_DESCRIPTION = "Описание программы 'Смотри на мир'."
REABILITATION_DESCRIPTION = "Описание программы 'Реабилитация'."
PSYCHOLOGICAL_HELP_DESCRIPTION = """
    Описание программы 'Психологическая помощь'.
"""
KIND_LESSONS_DESCRIPTION = "Описание программы 'Добрые уроки'."


PROGRAM_FOND = {
    "0": (
        "Смотри на мир",
        LOOK_AT_WORLD_DESCRIPTION,
        REQUIRED_DOCUMENTS
    ),
    "1": (
        "Реабилитация",
        REABILITATION_DESCRIPTION,
        REQUIRED_DOCUMENTS
    ),
    "2": (
        "Психологическая помощь",
        PSYCHOLOGICAL_HELP_DESCRIPTION,
        REQUIRED_DOCUMENTS,
    ),
    "3": (
        "Добрые уроки",
        KIND_LESSONS_DESCRIPTION,
        REQUIRED_DOCUMENTS
    ),
}


# Для перевода ответа кнопок выбора программы в читаемый вид
ALLIAS_DICT = {
    "Смотри на мир": "0",
    "Реабилитация": "1",
    "Психологическая помощь": "2",
    "Добрые уроки": "3",
}

# Спец символы для if в проверках адреса, диагноза
SPEC_SYM = ".,-"


# Клавиатуры
KEYBOARD_NEXT_BUTTON = [
    [
        "Продолжить",
    ]
]
KEYBOARD_FIX_VALUE = [
    [
        "Исправить",
    ]
]

MSG_PRESS_NEXT_BUTTON = """
    Нажмите продолжить.
"""
MSG_PRESS_FIX_VALUE = """
    Нажмите исправить.
"""
MSG_PRESS_ANY_BUTTON = "Отправьте, пожалуйста, мне любое сообщение."

MSG_FIRST_MENU = """
    Выберите программу фонда или же
    можете вернуться обратно в главное меню.
"""
MSG_SECOND_MENU = """
    Вы можете вступить, можете вернуться обратно или же в главное меню.
"""
MSG_THIRD_MENU = """
    Вы можете Отправить данные куратору,
    отредактировать их или же вернуться к выбору программ,
    но при этом ваши данне не будут сохранены.
"""

# Регулярки
REGEX_EMAIL = (
    r"^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"
)
REGEX_DATE_BIRTH = r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$"

# Клавиатуры с кнопками
MARKUP_NEXT = ReplyKeyboardMarkup(
    KEYBOARD_NEXT_BUTTON, one_time_keyboard=True, resize_keyboard=True
)
MARKUP_FIX = ReplyKeyboardMarkup(
    KEYBOARD_FIX_VALUE, one_time_keyboard=True, resize_keyboard=True
)

# Тема сообщения куратору от пользователя
SUBJECT = "Новая заявка на вступление в Фонд."
SUBJECT_ERROR = "ПОЛОМКА!"
