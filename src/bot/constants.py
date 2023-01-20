"""Constants."""


"""BOT BUTTONS."""

"""General."""
BTN_BEGIN = "Начать"
BTN_BACK = "Назад"
BTN_EDIT = "Редактировать"
BTN_SEND = "Отправить"
BTN_DONE = "Готово"
BTN_ANSWER = "Ответить"

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

"""Question"""
BTN_THEME = "Тема вопроса"
BTN_QUESTION = "Ваш вопрос"

"""Donation"""
BTN_REPORTS = "Годовые отчёты"
BTN_DONATION = "Пожертвование"


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

"""Volunteer."""
MSG_NEED_INFORMATION = "Далее необходимо предоставить информацию для куратора"
MSG_YOUR_HELP_OPTION = (
    "Вы можете предложить свой вариант помощи (необязательно).\n"
    "Нажмите /skip чтобы пропустить."
)

"""Question"""
MSG_QUESTION_NEED_INFORMATION = "Далее необходимо заполнить поля для вопроса:"
MSG_THEME = "Введите тему вопроса"
MSG_QUESTION = "Задайте ваш вопрос"
MSG_QUESTION_SENT = "Ваш вопрос отправлен."
MSG_QUESTION_ERROR_SENT = "Ошибка отправки вопроса."

"""Donation"""
MSG_DONATION = "Отчёты и пожертвование"


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