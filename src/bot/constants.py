"""Constants."""

"""BOT BUTTONS."""

"""General."""
BTN_BEGIN = "Начать"
BTN_BACK = "Назад"
BTN_EDIT = "Редактировать"
BTN_SEND = "Отправить"
BTN_DONE = "Готово"
BTN_MENU = "В главное меню"
BTN_ANSWER = "Ответить"
BIN_MAIN_MENU = "Главное меню"

"""Person."""
BTN_FULL_NAME = "Ф.И.О."
BTN_NAME = "Ваше имя"
BTN_BIRTHDAY = "Дата рождения"
BTN_CITY = "Город"
BTN_PHONE = "Телефон"
BTN_EMAIL = "Email"

"""Main Menu."""
BTN_TO_PARENTS_CHAT = "Хочу попасть в родительский чат"
BTN_TO_FUND = "Заявка в фонд"
BTN_TO_VOLUNTEER = "Хочу стать волонтёром"
BTN_TO_TELL_ABOUT_FUND = "Рассказать о Фонде своим друзьям"
BTN_TO_DONATION = "Пожертвование"
BTN_TO_OUR_EVENTS = "Наши события"
BTN_TO_ASK_A_QUESTION = "Задать вопрос"
BTN_TO_ABOUT_FUND = "О Фонде"

"""Volunteer."""
BTN_YOUR_HELP_OPTION = "Ваш вариант помощи"

"""Social links"""
BTN_WEBSITE = "Интернет сайт"
BTN_VK = "VK"
BTN_INSTAGRAM = "Instagram"
BTN_FACEBOOK = "Facebook"
BTN_TG_CHANNEL = "Новостной канал в Телеграм"
BTN_TG_BOT = "Приглашение в чат бот"

"""DONATION"""
"""Question"""
BTN_THEME = "Тема вопроса"
BTN_QUESTION = "Ваш вопрос"

"""Donation"""
BTN_REPORTS = "Годовые отчёты"
BTN_DONATION = "Пожертвование"

"""ABOUT"""
BTN_WHO_ARE_WE = "Кто мы?"
BTN_PROBLEM_SOLVING = "Какую социальную проблему мы решаем?"
BTN_WHAT_PROBLEM_SOLVING = "Как мы её решаем?"
BTN_LIFE_CHANGE = "Как мы меняем жизнь людей?"
BTN_WHAT_IS_DONE = "Что мы уже сделали?"
BTN_DONATION_NEED = "Зачем нужны пожертвования?"
BTN_SUCCESS = "История успеха"

"""Video"""
BTN_SUCCESS_VIDEO1 = "Лучик добра"
BTN_SUCCESS_VIDEO2 = "Фотосессия к 8 марта в г.Электросталь"
BTN_SUCCESS_VIDEO3 = "Сбор на операцию для маленькой Хаёт завершен!"
BTN_SUCCESS_VIDEO4 = "Праздник в честь 3-летия Фонда Провидение"
BTN_SUCCESS_VIDEO5 = "С Днем Защиты детей"


"""BOT MESSAGES."""

"""General."""
MSG_FULL_NAME = "Фамилия, Имя, Отчество?"
MSG_NAME = "Как к вам обращаться?"
MSG_BIRTHDAY = "Дата рождения?"
MSG_CITY = "Город проживания?"
MSG_PHONE = "Номер телефона?"
MSG_EMAIL = "Email?"
MSG_REQUEST_SENT = "Ваша заявка отправлена."
MSG_SENDING_ERROR = "Ошибка отправки email!"
MSG_GOODBYE = (
    "До свидания! Будем рады видеть Вас на нашем сайте!\n"
    "https://fond-providenie.ru\n"
    "Нажмите /start для повторного запуска"
)
MSG_CHOOSE_TO_EDIT = "Выберите для редактирования:"
MSG_ENTER_NEW_VALUE = "Введите новое значение:"
MSG_NO_DATA = "Нет данных."

"""MENU"""
MSG_START = (
    "Фонд помогает всем детям с нарушениями зрения"
    " независимо от места рождения и поддерживает семьи,"
    " где растут дети с инвалидностью."
)

"""TELL_ABOUT"""
MSG_TELL_ABOUT = "Выберите интересующую вас соцсеть/страницу"


"""EVENTS"""
MSG_EVENTS = "get_events"

"""Volunteer."""
MSG_NEED_INFORMATION = "Далее необходимо предоставить информацию для куратора"
MSG_YOUR_HELP_OPTION = (
    "Вы можете предложить свой вариант помощи (необязательно).\n"
    "Нажмите /skip чтобы пропустить."
)

"""Social links"""
MSG_WEBSITE = "https://fond-providenie.ru/"
MSG_VK = "https://vk.com/fond_providenie"
MSG_INSTAGRAM = "https://vk.com/fond_providenie"
MSG_FACEBOOK = "https://www.facebook.com/fond.providenie/"
MSG_TG_CHANNEL = "https://t.me/providenie_fond"
MSG_TG_BOT = "TODO"

"""DONATION"""
"""Question"""
MSG_QUESTION_NEED_INFORMATION = "Далее необходимо заполнить поля для вопроса:"
MSG_THEME = "Введите тему вопроса"
MSG_QUESTION = "Задайте ваш вопрос"
MSG_QUESTION_SENT = "Ваш вопрос отправлен."
MSG_QUESTION_ERROR_SENT = "Ошибка отправки вопроса."

"""Donation"""
MSG_DONATION = "Отчёты и пожертвование"

"""About"""
MSG_ABOUT = "Информация о фонде"
MSG_ABOUT_SUCCESS = "Видео успехов фонда"


"""LOG MESSAGES."""

LOG_BOT_BLOCKED_BY_USER = "Бот заблокирован пользователем"
LOG_ERROR_IN_RESPONSE = "Ошибка при ответе на сообщение"
ERROR_CANT_SEND_MSG_TO_EMAIL = (
    "Не удаётся отправить сообщение на email куратора!"
)
SUCCESSFUL_SENDING_MSG = "Сообщение отправлено куратору."

"""URLS"""

"""DONATION"""
URL_REPORTS = "https://fond-providenie.ru/docs/"
URL_DONATION = (
    "https://fond-providenie.ru/help-chidren/sdelat-pozhertovanie"
    "/sdelat-pozhertvovanie-s-bankovskoj-karty/"
)

"""ABOUT"""
URL_WHO_ARE_WE = "https://telegra.ph/Kto-my-02-06"
URL_PROBLEM_SOLVING = (
    "https://telegra.ph/Kakuyu-socialnuyu-problemu-my-reshaem-02-06"
)
URL_WHAT_PROBLEM_SOLVING = "https://telegra.ph/Kak-my-eyo-reshaem-02-06"
URL_LIFE_CHANGE = "https://telegra.ph/Kak-my-menyaem-zhizn-lyudej-02-06"
URL_WHAT_IS_DONE = (
    "https://telegra.ph/"
    "CHto-uzhe-sdelano-Kto-obrashchaetsya-za-pomoshchyu-02-06"
)
URL_DONATION_NEED = "https://telegra.ph/Zachem-nuzhny-pozhertvovaniya-02-06"


"""ABOUT_SUCCESS"""
URL_VIDEO_1 = "https://youtu.be/n-hByd_oiIo"
URL_VIDEO_2 = "https://youtu.be/NG4QUO-hvCk"
URL_VIDEO_3 = "https://youtu.be/cAQayg_ZNok"
URL_VIDEO_4 = "https://youtu.be/26mYPRE4BQo"
URL_VIDEO_5 = "https://youtu.be/CINnVYp6hQI"

"""Chats"""
"""Get_data"""
MSG_CHAT_PARENTS_NAME = "Фамилия, имя, отчество мамы (или папы)?"
MSG_CHAT_PARENTS_PHONE = "Номер телефона мамы (или папы)?"
MSG_CHAT_CHILD_NAME = "Фамилия, имя, отчество ребенка?"
MSG_CHAT_CHILD_BIRTHDAY = "Дата рождения ребенка?"
MSG_CHAT_CHILD_PLACE_BIRTHDAY = "Место рождения ребенка?"
MSG_CHAT_CHILD_TERM = "Срок беременности при рождении ребенка?"
MSG_CHAT_CHILD_WEIGHT = "Вес ребенка при рождении?"
MSG_CHAT_CHILD_HEIGHT = "Рост ребенка при рождении?"
MSG_CHAT_CHILD_DIAGNOSE = "Диагнозы у ребенка?"
MSG_CHAT_CHILD_OPERATION = "Были ли проведены операции? Дата и место операций?"
MSG_CHAT_ABOUT_FOND = "Как Вы узнали о фонде?"
MSG_CHAT_GRANDMOTHERS_NAME = "Фамилия, имя, отчество бабушки (или дедушки)?"
MSG_CHAT_GRANDMOTHERS_PHONE = "Номер телефона бабушки (или дедушки)?"
MSG_CHAT_GRANDMOTHERS_GRANDCHILD = "Фамилия, имя, отчество внука (внучки)?"

MSG_CHAT_ENTER = "Вступить в чат"

MSG_CHAT_EDIT_NAME = "Фамилия, имя, отчество"
MSG_CHAT_EDIT_PHONE = "Номер телефона"
MSG_CHAT_EDIT_CHILD_NAME = "Фамилия, имя, отчество ребенка"
MSG_CHAT_EDIT_CHILD_BIRTHDAY = "Дата рождения"
MSG_CHAT_EDIT_CHILD_PLACE_BIRTHDAY = "Место рождения"
MSG_CHAT_EDIT_CHILD_TERM = "Срок беременности"
MSG_CHAT_EDIT_CHILD_WEIGHT = "Вес"
MSG_CHAT_EDIT_CHILD_HEIGHT = "Рост"
MSG_CHAT_EDIT_CHILD_DIAGNOSE = "Диагнозы"
MSG_CHAT_EDIT_CHILD_OPERATION = "Операции"
MSG_CHAT_EDIT_ABOUT_FOND = "Как узнали о фонде"

"""BOT TEXT INFO."""

TXT_MEIN_MENU = (
    "Фонд помогает всем детям с нарушениями зрения"
    " независимо от места рождения и поддерживает"
    " семьи, где растут дети с инвалидностью."
)

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
    "bad_people_in_family": """
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
    "birthday": "Введите дату рождения ребёнка. (Д.М.ГГГГ)",
    "place_birth": "Введите место рождения ребёнка.",
    "birth_date": "Введите срок на котором родился ребёнок. (Неделя, числом)",
    "weight": "Введите вес ребёнка. (Числом)",
    "height": "Введите рост ребёнка. (Числом)",
    "diagnosis": """
        Введите диагнозы ребёнка.
        (Через запятую, при наличии нескольких)""",
    "how_found_fund": "Откуда вы узнали о нашем фонде?",
    "which_fund": "Вам помогали фонды раньше? Если да, то какие?",
    "fund_now": """
        Состоите ли вы в данный момент в каком-либо фонде,
        если да, то напишите название фонда?""",
}

BUTTONS_TEXT = {
    "fio_mother": "ФИО мамы",
    "phone_number": "Телефон",
    "email": "Email",
    "fio_child": "ФИО ребёнка",
    "how_many_people": "Количество членов семьи",
    "city": "Город",
    "address": "Адрес",
    "birthday": "Дата рождения ребёнка",
    "place_birth": "Место рождения ребёнка",
    "birth_date": "Срок рождения",
    "weight": "Вес",
    "height": "Рост",
    "diagnosis": "Диагнозы",
    "how_found_fund": "Как узнали о нас",
    "which_fund": "В каком фонде сейчас",
    "fund_now": "Какие фонды помогали",
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
    Так же нужно будет подготовить документы.\n
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

# Здесь описания программ фонда
LOOK_AT_WORLD_DESCRIPTION = "Описание программы 'Смотри на мир'."
REABILITATION_DESCRIPTION = "Описание программы 'Реабилитация'."
PSYCHOLOGICAL_HELP_DESCRIPTION = """
    Описание программы 'Психологическая помощь'.
"""
KIND_LESSONS_DESCRIPTION = "Описание программы 'Добрые уроки'."

# Спец символы для if в проверках адреса, диагноза
SPEC_SYM = ".,-"

# Конка исправить
KEYBOARD_FIX_VALUE = [
    [
        "Исправить",
    ]
]

MSG_PRESS_FIX_VALUE = """
    Нажмите исправить.
"""

# Текстовые выводы при смене уровня
MSG_FIRST_MENU = """
    Выбрать программу фонда или
    вернуться обратно в главное меню.
"""
MSG_SECOND_MENU = """
    Вы можете отправить заявку в фонд,
    вернуться обратно к выбору фонда или в главное меню.
"""
MSG_THIRD_MENU = """
    Отправить данные куратору,
    отредактировать их или вернуться к выбору программ,
    но при этом ваши данные не будут сохранены.
"""

MSG_EDIT = "Выберите пункт, который вы бы хотели изменить"

MSG_GOODBYE = """
До свидания! Будем рады видеть Вас на нашем сайте!\n
https://fond-providenie.ru\n
Нажмите /start для повторного запуска
"""

# Регулярки
REGEX_EMAIL = (
    r"^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"
)
REGEX_BIRTHDAY = r"^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}$"

# Тема сообщения куратору от пользователя
SUBJECT = "Новая заявка на вступление в Фонд."
SUBJECT_ERROR = "ПОЛОМКА!"

# Ключи скрытые для вывода
SECRET_KEY = ["START_OVER", "Programm", "FLAGS"]
