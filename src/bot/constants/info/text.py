SHARE = (
    "\n\nЧтобы оставаться в курсе последних новостей, рекомендуем Вам подписаться на наши страницы в социальных сетях: "
    "\n\n<a href='https://fond-providenie.ru/'>Сайт Благотворительного Фонда “Провидение”</a>"
    "\n<a href='https://vk.com/fond_providenie '>Группа Вконтакте</a>"
    "\n<a href='https://zen.yandex.ru/fond_providenie'>Наша страница на Яндекс.Дзен</a>"
    "\n<a href='https://t.me/providenie_fond'>Новостной канал Telegram</a>"
    "\n<a href='https://www.instagram.com/fond_providenie/'>Наша страница в Instagram</a>"
    "\n<a href='https://dobro.mail.ru/funds/blagotvoritelnyij-fond-pomoschi-nedonoshennyim-detyam-i-ih-semyam-providenie-2/'>Наша страница на Mail.ru</a>"
    "\n<a href='https://youtube.com/channel/UC_co5lBatw_pA2DceKCqZfg'>Наш канал на Youtube</a>"
)

# MAIN MENU
START = (
    "Здравствуйте! Добро пожаловать!"
    "\n\nЯ бот - помощник Благотворительного Фонда «Провидение»."
    "\nМы помогаем детям, родившимся раньше срока, лучше видеть, слышать и разговаривать, а также поддерживаем их родителей."
    "\n\nНаша миссия – спасти зрение детей, помочь им избежать инвалидности и улучшить качество жизни их семей."
    f"{SHARE}"
)

STOP = "До скорых встреч!"

MAIN_MENU = "Главное меню Благотворительного Фонда “Провидение”"


# MAIN COMMANDS
START_CMD = "Начать работу"
MENU_CMD = "Перейти в главное меню"
CANCEL_CMD = "Отменить текущее действие"
STOP_CMD = "Завершение работы"


# MAIN BUTTONS
BACK = "Назад"
FOLLOW_LINK = "Перейти"
MAIN_BACK = "Главное меню"
START_FORM = "Заполнить анкету"
SEND_FORM = "Отправить"
EDIT_FORM = "Редактировать"


# SHOW FORM DATA
FORM = "Анкета"
CHOICE = "Выбор"
APPLICATION_DATE = "Дата заявки"
SELECT_EDIT = "Выберите для редактирования:"
MESSAGE_MARKDOWN = "HTML"
SHOW_DATA_TEMPLATE = "<b><u>{title}</u></b>:\n{value}\n\n"
INPUT_ERROR_TEMPLATE = "<b>Некорректно введены данные!</b>\n\n{hint}"
DATE_TEMPLATE = "%d.%m.%Y"


# DOCUMENTS FOR FORMS
REQUIRED_DOCUMENTS = f"""
<b>Внимание</b>!
Cписок документов, которые необходимо прислать координатору Фонда на почту terekhova@fond-provideniе.ru:
\n- Справка о многодетности, малообеспеченности, инвалидности (фото/скан)
- Справка 2-НДФЛ родителей или любая форма справки, подтверждающая доход родителей (фото/скан)
- Выписка с рекомендациями врача на запрашиваемое лечение (фото/скан)
- Свидетельство о рождении ребёнка (фото/скан)
- Паспорт родителей (фото/скан)
- Фото (не менее 10 шт) и видео ребёнка
- Полный текст вашей истории для нашего сайта
{SHARE}
"""


# MAIL CONSTANTS
MAIL_SEND_OK_MESSAGE = "Запрос успешно отправлен"
MAIL_SEND_ERROR_MESSAGE = "Ошибка: Невозможно отправить запрос"

# REGEXP
REGEX_PHONE = r"^(?:\+)?[0-9]\d{10,14}$"
REGEX_FULL_NAME = r"^([А-Яа-яЁё\-]+\b {,3}){2,}$"
REGEX_TXT_WITHOUT_LATIN = r"[^a-zA-Z]+"

# Quantity of family members (variants)
FAMILY_MEMBERS = r"(?i)^(не)?\s?полная$"
