import re
from datetime import date

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import ContextTypes, ConversationHandler

from core.email import bot_send_email_to_curator
from core.logger import logger


# Константы этапов разговора
(
    LOOK_WORLD_PROGRAMM, REABILITATION_PROGRAMM,
    PSIHO_PROGRAMM, KIND_ARMS_PROGRAMM
) = map(chr, range(4))

(
    FIO_MOTHER, PHONE, EMAIL, FIO_CHILD, HOW_MANY_PEOPLES, CITY, 
    ADRESS, DATE_BIRTH, LOCAL_OF_BIRTH, SPACING, WEIGHT, HEIGHT,
    DIAGNOZES, DATE_OF_APPLICATION, HOW_FIND_US, WHICH_FOND,
    WHICH_FOND_WAS_PREVIOUSLY, START_OVER
) = map(chr, range(4, 22))


CHOISE_PROGRAMM, JOIN_TO_PROGRAMM = map(chr, range(22, 24))
(
    JOIN_BUTTON, BAD_ANSWER_SECOND_LEVEL, SHOW_INFORMATION,
    CONFIRM_AND_SEND, END_SECOND_LEVEL, SEND_CHANGE_END,
    CHANGE_DATES, MESSAGE_SENT_SUCCESSFULLY, END_FIRST_LEVEL,
    EDIT_MODE, SHOW_EDIT_INFORMATIONS, SAY_YES, SAY_NO,
    QUESTION_THIRD_MENU, BAD_FIO_MOTHER, BAD_VALUES, RETURN_MOTHER_FIO,
    GO_SECOND_LEVEL
) = map(chr, range(24, 42))

EDIT_PHONE, EDIT_USER_DATES, PLACE_BIRTH = map(chr, range(42, 45))

END = ConversationHandler.END


# Различные ответы, вопросы, описание и документы
ANSWERS_DICT = {
    "bad_answer": "Неопределено, всё исправится куратором чуть позже.",
    "bad_fio_mother": "Неверно введено ФИО, пожалуйста, нажмите исправить.",
    "bad_phone_number": "Неверно введён номер телефона, пожалуйста, нажмите исправить.",
    "bad_email": "Неверно введён email, пожалуйста, нажмите исправить.",
    "bad_child_fio": "Неверно введено ФИО ребёнка, пожалуйста, нажмите исправить.",
    "bad_people_in_famaly": "Неверно введено количество членов семьи, пожалуйста, нажмите исправить.",
    "bad_city": "Неверно введено название города, пожалуйста, нажмите исправить",
    "bad_adress": "Неверно введён адрес, пожалуйста, нажмите исправить.",
    "bad_date_birth": "Неверно введена дата рождения ребёнка, пожалуйста, нажмите исправить.",
    "bad_place_birth": "Неверно введено место рождения ребёнка, пожалуйста, нажмите исправить.",
    "bad_spacing": "Неверно введён срок рождения ребёнка, пожалуйста, нажмите исправить.",
    "bad_wight": "Неверно введён вес ребёнка, пожалуйста, нажмите исправить.",
    "bad_hight": "Неверно введён рост ребёнка, пожалуйста, нажмите исправить.",
    "bad_diagnoz": "Неверно введён диагноз ребёнка, пожалуйста, нажмите исправить",
    "bad_date_application": "Неверно введена дата обращения, пожалуйста, нажмите исправить.",
}

QUATIONS_DICT = {
    "fio_mother": "Введите ФИО мамы.",
    "phone_number": "Введите телефон.(Начиная с 8)",
    "email": "Введите ваш email.",
    "fio_child": "Введите ФИО ребёнка.",
    "how_many_people": "Введите количество членов семьи. (числом)",
    "city": "Введите город проживания.",
    "adress": "Введите адрес проживания.",
    "date_birth": "Введите дату рождения ребёнка. (ДД.ММ.ГГГГ)",
    "place_birth": "Введите место рождения ребёнка.",
    "spacing": "Введите срок на котором родился ребёнок. (Неделя, числом)",
    "wight": "Введите вес ребёнка. (Числом)",
    "hight": "Введите рост ребёнка. (Числом)",
    "diagnoz": "Введите диагнозы ребёнка. (Через запятую, при наличии нескольких)",
    "date_aplication": "Введите дату обращения в Фонд. (ДД.ММ.ГГГГ)",
    "how_find_fond": "Откуда вы узнали о нашем фонде?",
    "which_fond": "Вам помогали фонды раньше? Если да, то какие?",
    "fond_now": """Состоите ли вы в данный момент в каком-либо фонде, 
        если да, то напишите название фонда?""",
}

MESSAGE_SUCCESSFUL_DEPARTURE_TO_CURATOR = """
    Ваши данные успешно отправлены куратору.
    Ожидайте сообщения от куратора.
    Так же нужно будет подготовить документы:\n
"""


REQUIRED_DOCUMENTS = """
Необходимые документы:\n
- Справка о многодетности, малообеспеченности, инвалидности (фото).\n
- Справка 2 НДФЛ родителей или любая форма справки, подтверждающая ДОХОД РОДИТЕЛЕЙ\n
- Выписка с рекомендациями (фото/скан)\n
- Свидетельство о рождении (фото/скан)\n
- Паспорт (фото/скан)\n
- Счёт на лечение (какое лечение требуется, стоимость) или ссылка на то, что необходимо приобрести\n
"""


LOOK_AT_WORLD_DESCRIPTION = "Описание программы 'Смотри на мир'."
REABILITATION_DESCRIPTION = "Описание программы 'Реабилитация'."
PSYCHOLOGICAL_HELP_DESCRIPTION = "Описание программы 'Психологическая помощь'."
KIND_HANDS_DESCRIPTION = "Описание программы 'Добрые уроки'."


PROGRAMM_FOND = {
    "\x00": ("Смотри на мир" ,LOOK_AT_WORLD_DESCRIPTION, REQUIRED_DOCUMENTS),
    "\x01": ("Реабилитация", REABILITATION_DESCRIPTION, REQUIRED_DOCUMENTS),
    "\x02": ("Психологическая помощь", PSYCHOLOGICAL_HELP_DESCRIPTION, REQUIRED_DOCUMENTS),
    "\x03": ("Добрые уроки", KIND_HANDS_DESCRIPTION, REQUIRED_DOCUMENTS)
}


# Для перевода ответа кнопок выбора программы в читаемый вид 
ALLIAS_DICT = {
    "Смотри на мир": "\x00",
    "Реабилитация": "\x01",
    "Психологическая помощь": "\x02",
    "Добрые уроки": "\x03",
}

# Спец символы для if в проверках адреса, диагноза
SPEC_SYM = ".,-"


# Клавиатуры
KEYBOARD_NEXT_BUTTON = [["Продолжить",]]
KEYBOARD_FIX_VALUE = [["Исправить",]]

MSG_PRESS_NEXT_BUTTON = "Нажмите, пожалуйста, продолжить."
MSG_PRESS_FIX_VALUE = "Нажмите, пожалуйста, исправить."
MSG_PRESS_ANY_BUTTON = "Отправьте, пожалуйста, мне любое сообщение."

MARKUP_NEXT = ReplyKeyboardMarkup(
    KEYBOARD_NEXT_BUTTON,
    one_time_keyboard=True,
    resize_keyboard=True
)
MARKUP_FIX = ReplyKeyboardMarkup(
    KEYBOARD_FIX_VALUE,
    one_time_keyboard=True,
    resize_keyboard=True
)


# Регулярки
REGEX_EMAIL = r"^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"
REGEX_DATE_BIRTH = r"^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$"


# Флаги, для направления логики ответов
class Flags:
    """Флаги:
    Режима редактирования данных,
    Режим первого старта,
    Режим невалидного ввода.
    """
    edit_mode_first_flag = False
    edit_mode_second_flag = False
    first_start = False
    bad_request = False

    def changing_edit_mode_first(self, edit_mode: bool):
        """Смена флага edit_mode_first_flag."""
        if isinstance(edit_mode, bool):
            Flags.edit_mode_first_flag = edit_mode
        else:
            msg = f'Неверный тип флага {edit_mode}!'
            logger.error(msg)

    def changing_edit_mode_second(self, edit_mode: bool):
        """Смена флага edit_mode_second_flag."""
        if isinstance(edit_mode, bool):
            Flags.edit_mode_second_flag = edit_mode
        else:
            msg = f'Неверный тип флага {edit_mode}!'
            logger.error(msg)

    def changing_first_start(self, first_start: bool):
        """Смена флага first_start."""
        if isinstance(first_start, bool):
            Flags.first_start = first_start
        else:
            msg = f'Неверный тип флага {first_start}!'
            logger.error(msg)

    def changing_bad_request(self, bad_request: bool):
        """Смена флага bad_request."""
        if isinstance(bad_request, bool):
            Flags.bad_request = bad_request
        else:
            msg = f'Неверный тип флага {bad_request}!'
            logger.error(msg)


# Создание объекта флагов
FLAGS_OBJ = Flags()


# Подпрограммы
def clean_dictionary(context, save_values=[None]) -> None:
    """Очистка словаря."""
    for key in context:
        if not key in save_values:
            context[key] = ""
    # logger.info(context)


# Валидаторы
def checking_not_digits(data: str) -> bool:
    """Проверка текстовых значений."""
    if (all(x.isalpha() or x.isspace() or x in SPEC_SYM for x in data) and 
            data != "" and len(data) < 100):
        return True
    return False


def checking_not_phone_number(data: str) -> bool:
    """Проверка телефонного номера."""
    if data.isdigit() and len(data) == 11:
        return True
    return False


def checking_email(data: str) -> bool:
    """Проверка email."""
    return bool(re.match(REGEX_EMAIL, data))


def checking_number_people_in_family(data: str) -> bool:
    """
    Проверка на число.
    Для колличества членов в семье
    """
    if data.isdigit() and int(data) > 0 and int(data) <= 52:
        return True
    return False


def checking_date_birth(data: str) -> bool:
    """Проверка правильности ввода даты рождения."""
    flag = True
    date_now = date.today()

    if bool(re.match(REGEX_DATE_BIRTH, data)):
        date_split_list = data.split(".")
        if int(date_split_list[0]) < 1 or int(date_split_list[0]) > 31:
            flag = False
        if int(date_split_list[1]) < 1 or int(date_split_list[1]) > 12:
            flag = False
        if int(date_split_list[2]) < 1950 or int(date_split_list[2]) > date_now.year:
            flag = False
    else:
        flag = False
    return flag


def checking_wight_and_hight(data: str) -> bool:
    """Проверка правильности ввода веса и роста."""
    if data.isdigit() and int(data) > 0 and int(data) < 100:
        return True
    return False



# Здесь начинаются обработчики кнопок и ответов на вопросы
async def application_to_the_fond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Вывод кнопок программ фонда."""

    buttons = [
        [
            InlineKeyboardButton(text="Смотри на мир", callback_data=str(LOOK_WORLD_PROGRAMM)),
            InlineKeyboardButton(text="Реабилитация", callback_data=str(REABILITATION_PROGRAMM)),
        ],

        [
            InlineKeyboardButton(text="Психологическая помощь", callback_data=str(PSIHO_PROGRAMM)),
            InlineKeyboardButton(text="Добрые уроки", callback_data=str(KIND_ARMS_PROGRAMM))
        ],

        [
            InlineKeyboardButton(text="Главное меню", callback_data=str(END)),
        ],

    ]

    keyboard = InlineKeyboardMarkup(buttons)
    message = "Выберите программу фонда или же можете вернуться обратно в главное меню."

    if FLAGS_OBJ.first_start:   
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=message, reply_markup=keyboard)
        
        logger.info(context.user_data["Программа фонда"])
    else:
        await update.message.reply_text(text=message, reply_markup=keyboard)
        FLAGS_OBJ.changing_first_start(True)


    return CHOISE_PROGRAMM


async def join_or_not_to_programm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Вывод информации о фонде, а также кнопок:
    Вступить, назад, в главное меню.
    """
    query = update.callback_query
    await query.answer()

    if not FLAGS_OBJ.edit_mode_first_flag:    
        data = update.callback_query.data

        if data in PROGRAMM_FOND:
            message_about_fond_and_documations = (
                f"{PROGRAMM_FOND[data][0]}\n" +
                f"{PROGRAMM_FOND[data][1]}\n" +
                f"{PROGRAMM_FOND[data][2]}\n"    
            )
            context.user_data["Программа фонда"] = PROGRAMM_FOND[data][0]
        else:
            context.user_data["Программа фонда"] = ANSWERS_DICT["bad_answer"]
        
    else:
        dates_about_fond = PROGRAMM_FOND[ALLIAS_DICT[context.user_data["Программа фонда"]]]
        message_about_fond_and_documations = (
                f"{dates_about_fond[0]}\n" +
                f"{dates_about_fond[1]}\n" +
                f"{dates_about_fond[2]}\n"    
            )

        FLAGS_OBJ.changing_edit_mode_first(False)


    buttons = [
        [
            InlineKeyboardButton(text="Вступить", callback_data=str(JOIN_BUTTON)),
            InlineKeyboardButton(text="Назад", callback_data=str(END)),
        ],

        [
            InlineKeyboardButton(text="Главное меню", callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    message = "Вы можете вступить, можете вернуться обратно или же в главное меню."
    await query.edit_message_text(
        text=message_about_fond_and_documations + message,
        reply_markup=keyboard,
    )

    return JOIN_TO_PROGRAMM


async def go_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Переход на второй уровень."""
    query = update.callback_query
    await query.edit_message_text(text=MSG_PRESS_ANY_BUTTON)

    return GO_SECOND_LEVEL


async def asking_fio_mother(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение фамилии мамы."""
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["fio_mother"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return FIO_MOTHER

    await update.message.reply_text(QUATIONS_DICT["fio_mother"])

    return FIO_MOTHER


async def asking_phone_mother(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение телефона мамы."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(QUATIONS_DICT["phone_number"])
        FLAGS_OBJ.changing_bad_request(False)
        return PHONE

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["phone_number"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return PHONE

    fio = update.message.text
    
    if not checking_not_digits(fio):
        await update.message.reply_text(text=ANSWERS_DICT["bad_fio_mother"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)

        return RETURN_MOTHER_FIO

    context.user_data["ФИО мамы"] = fio.title()
    logger.info(f"ФИО мамы: {fio}")
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )

        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["phone_number"])

    return PHONE


async def asking_email_mother(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение email мамы."""
    if FLAGS_OBJ.bad_request: 
        await update.message.reply_text(QUATIONS_DICT["email"])
        FLAGS_OBJ.changing_bad_request(False)
        return EMAIL

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["email"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return EMAIL


    phone_number = update.message.text
    
    if not checking_not_phone_number(phone_number):
        await update.message.reply_text(text=ANSWERS_DICT["bad_phone_number"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return FIO_MOTHER

    context.user_data["Телефон"] = phone_number
    logger.info(f"Телефон мамы: {phone_number}")
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )

        return SHOW_EDIT_INFORMATIONS
    
    await update.message.reply_text(QUATIONS_DICT["email"])

    return EMAIL


async def asking_fio_child(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение ФИО ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(QUATIONS_DICT["fio_child"])
        FLAGS_OBJ.changing_bad_request(False)
        
        return FIO_CHILD
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["fio_child"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return FIO_CHILD
    
    email_mother = update.message.text
    logger.info(f"email в fio_children: flag - {FLAGS_OBJ.bad_request}")
    if not checking_email(email_mother):
        await update.message.reply_text(text=ANSWERS_DICT["bad_email"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)

        return PHONE

    context.user_data["Email"] = email_mother
    logger.info(f"Email мамы: {email_mother}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["fio_child"])

    return FIO_CHILD


async def asking_how_many_people_in_famaly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение количества членов семьи."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["how_many_people"])
        FLAGS_OBJ.changing_bad_request(False)
        return HOW_MANY_PEOPLES
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["how_many_people"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return HOW_MANY_PEOPLES

    fio_child = update.message.text
    logger.info(f"ФИО ребёнка: {fio_child}")

    if not checking_not_digits(fio_child):
        await update.message.reply_text(text=ANSWERS_DICT["bad_child_fio"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return EMAIL
    

    context.user_data["ФИО ребёнка"] = fio_child.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["how_many_people"])

    return HOW_MANY_PEOPLES


async def asking_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение города проживания."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["city"])
        FLAGS_OBJ.changing_bad_request(False)
        return CITY

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["city"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return CITY

    how_many_pioples = update.message.text
    
    
    if not checking_number_people_in_family(how_many_pioples):
        await update.message.reply_text(text=ANSWERS_DICT["bad_people_in_famaly"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return FIO_CHILD

    context.user_data["Сколько членов семьи"] = how_many_pioples
    logger.info(f"Членов семьи: {how_many_pioples}")
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["city"])

    return CITY


async def asking_adress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение адреса проживания."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["adress"])
        FLAGS_OBJ.changing_bad_request(False)
        return ADRESS
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["adress"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return ADRESS
    
    city = update.message.text
    

    if not checking_not_digits(city):
        await update.message.reply_text(text=ANSWERS_DICT["bad_city"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return HOW_MANY_PEOPLES


    context.user_data["Город"] = city.title()
    logger.info(f"Город проживания: {city}")
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["adress"])

    return ADRESS


async def asking_child_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение дня рождения ребенка."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["date_birth"])
        FLAGS_OBJ.changing_bad_request(False)
        return DATE_BIRTH
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["date_birth"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return DATE_BIRTH
    
    adress = update.message.text


    context.user_data["Адрес"] = adress.title()
    logger.info(f"Адрес проживания: {adress}")
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["date_birth"])

    return DATE_BIRTH


async def asking_place_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение места рождения ребенка."""
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["place_birth"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return PLACE_BIRTH
    
    child_birthsday = update.message.text
    

    if not checking_date_birth(child_birthsday):
        await update.message.reply_text(text=ANSWERS_DICT["bad_date_birth"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return ADRESS
    
    context.user_data["Дата рождения ребёнка"] = child_birthsday
    logger.info(f"Дата рождения ребёнка: {child_birthsday}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["place_birth"])

    return PLACE_BIRTH


async def asking_spacing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение срока рождения ребёнка."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["spacing"])
        FLAGS_OBJ.changing_bad_request(False)
        return SPACING
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["spacing"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return SPACING

    place_birth = update.message.text
    
    context.user_data["Место рождения ребёнка"] = place_birth.title()
    logger.info(f"Место рождения ребёнка: {place_birth}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["spacing"])

    return SPACING


async def asking_child_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение веса ребёнка."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["wight"])
        FLAGS_OBJ.changing_bad_request(False)
        return WEIGHT

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["wight"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return WEIGHT

    spacing = update.message.text
    

    if not checking_number_people_in_family(spacing):
        await update.message.reply_text(text=ANSWERS_DICT["bad_spacing"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return PLACE_BIRTH

    context.user_data["Срок рождения ребёнка"] = spacing
    logger.info(f"Срок рождения ребёнка: {spacing}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["wight"])

    return WEIGHT


async def asking_child_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение роста ребёнка."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["hight"])
        FLAGS_OBJ.changing_bad_request(False)
        return HEIGHT
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["hight"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return HEIGHT

    child_weight = update.message.text
    

    if not checking_wight_and_hight(child_weight):
        await update.message.reply_text(text=ANSWERS_DICT["bad_wight"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return SPACING

    context.user_data["Вес"] = child_weight
    logger.info(f"Вес ребёнка: {child_weight}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["hight"])

    return HEIGHT


async def asking_child_diagnozes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение диагнозов ребёнка."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["diagnoz"])
        FLAGS_OBJ.changing_bad_request(False)
        return DIAGNOZES
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["diagnoz"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return DIAGNOZES

    child_height = update.message.text
    

    if not checking_wight_and_hight(child_height):
        await update.message.reply_text(text=ANSWERS_DICT["bad_hight"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return WEIGHT

    context.user_data["Рост"] = child_height
    logger.info(f"Рост ребёнка: {child_height}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["diagnoz"])

    return DIAGNOZES


async def asking_date_of_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение обращения в фонд."""
    if FLAGS_OBJ.bad_request:    
        await update.message.reply_text(QUATIONS_DICT["date_aplication"])
        FLAGS_OBJ.changing_bad_request(False)
        return DATE_OF_APPLICATION
    
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["date_aplication"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return DATE_OF_APPLICATION

    diagnozes = update.message.text
    

    if not checking_not_digits(diagnozes):
        await update.message.reply_text(text=ANSWERS_DICT["bad_diagnoz"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return HEIGHT

    context.user_data["Диагнозы"] = diagnozes.title()
    logger.info(f"Диагнозы ребёнка: {diagnozes}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["date_aplication"])

    return DATE_OF_APPLICATION


async def asking_how_find_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение информации о том, как нашли фонд."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["how_find_fond"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return HOW_FIND_US

    date_of_application = update.message.text
    

    if not checking_date_birth(date_of_application):
        await update.message.reply_text(text=ANSWERS_DICT["bad_date_application"], reply_markup=MARKUP_FIX)
        FLAGS_OBJ.changing_bad_request(True)
        return DIAGNOZES

    context.user_data["Дата обращения"] = date_of_application
    logger.info(f"Дата обращения в фонд: {date_of_application}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["how_find_fond"])

    return HOW_FIND_US


async def asking_which_fond_now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Получение информации о том, состоят ли ещё в 
    каком-либо фонде в данный момент.
    """

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["fond_now"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return WHICH_FOND

    how_find_us = update.message.text

    context.user_data["Как узнали о нас"] = how_find_us.title()
    logger.info(f"Как нашли фонд: {how_find_us}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["fond_now"])

    return WHICH_FOND


async def asking_which_fonds_halped(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение информации о том, какие фонды помогали раньше."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(QUATIONS_DICT["which_fond"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return WHICH_FOND_WAS_PREVIOUSLY

    which_fond_now = update.message.text
    
    context.user_data["В фонде сейчас"] = which_fond_now.title()
    logger.info(f"В каких фондах состоят в данный момент: {which_fond_now}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(QUATIONS_DICT["which_fond"])

    return WHICH_FOND_WAS_PREVIOUSLY


async def show_user_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Отображение пользователю пролученной информации."""

    which_fonds_halped = update.message.text
    
    context.user_data["Фонды помогали"] = which_fonds_halped.title()
    logger.info(f"Какие фонды помогали ранее: {which_fonds_halped}")

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
        )
        return SHOW_EDIT_INFORMATIONS

    for key, date in context.user_data.items():
        await update.message.reply_text(f"{key}: {date}")

    await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
    )

    return SHOW_INFORMATION
    

async def show_user_edit_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Отображение пользователю обновленной информации после редактирования."""

    for key, date in context.user_data.items():
        await update.message.reply_text(f"{key}: {date}")

    await update.message.reply_text(
            MSG_PRESS_NEXT_BUTTON,
            reply_markup=MARKUP_NEXT,
    )

    return SHOW_INFORMATION



async def send_or_change_dates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню с выбором дальнейших действий:
    - Отправить данные куратору
    - Изщменить данные
    - Назад
    """

    buttons = [
        [
            InlineKeyboardButton(text="Подтвердить и отправить", callback_data=str(CONFIRM_AND_SEND)), 
        ],

        [
            InlineKeyboardButton(text="Изменить данные", callback_data=str(CHANGE_DATES)),
            InlineKeyboardButton(text="Назад", callback_data=str(END_SECOND_LEVEL)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    message = """
    Вы можете Отправить данные куратору, 
    отредактировать их или же вернуться к выбору программ, 
    но при этом ваши данне не будут сохранены."""

    await update.message.reply_text(text=message, reply_markup=keyboard)

    return SEND_CHANGE_END


async def send_message_to_curator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отправка сообщения куратору с данными. Пока без фотографии/сканов. """

    query = update.callback_query
    await query.answer()
    # СДЕСЬ ДОЛЖНА БЫТЬ ФУНКЦИЯ ОТПРАВКИ ДАННЫХ
    subject = "Новая заявка на вступление в Фонд."
    try:
        bot_send_email_to_curator(subject, context.user_data)
        logger.info(f"На отправку ушёл словарь: {context.user_data}")
    except Exception as ex:
        logger.error(ex)

    documents = "Вам сообщит куратор."

    if context.user_data["Программа фонда"] in ALLIAS_DICT:
        documents = PROGRAMM_FOND[ALLIAS_DICT[context.user_data["Программа фонда"]]][2]

    button = [
        [
            InlineKeyboardButton(
                text="Назад в основное меню",
                callback_data=str(END)), 
        ],
    ]

    keyboard = InlineKeyboardMarkup(button)

    await query.edit_message_text(
        text=MESSAGE_SUCCESSFUL_DEPARTURE_TO_CURATOR + documents,
        reply_markup=keyboard
    )

    return MESSAGE_SENT_SUCCESSFULLY


async def change_dates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Изменение данных пользователя через кнопки."""
    query = update.callback_query

    await query.answer()


    buttons = [
        [
            InlineKeyboardButton(text="ФИО мамы", callback_data=str(FIO_MOTHER)),
            InlineKeyboardButton(text="Телефон", callback_data=str(PHONE)),
            InlineKeyboardButton(text="Email", callback_data=str(EMAIL)),
        ],

        [
            InlineKeyboardButton(text="ФИО ребёнка", callback_data=str(FIO_CHILD)),
            InlineKeyboardButton(text="Количество членов семьи", callback_data=str(HOW_MANY_PEOPLES)),
            InlineKeyboardButton(text="Город", callback_data=str(CITY))
        ],

        [
            InlineKeyboardButton(text="Адрес", callback_data=str(ADRESS)),
            InlineKeyboardButton(text="Дата рождения ребёнка", callback_data=str(DATE_BIRTH)),
            InlineKeyboardButton(text="Место рождения ребёнка", callback_data=str(PLACE_BIRTH)),
        ],

        [
            InlineKeyboardButton(text="Срок рождения", callback_data=str(SPACING)),
            InlineKeyboardButton(text="Вес", callback_data=str(WEIGHT)),
            InlineKeyboardButton(text="Рост", callback_data=str(HEIGHT)),
        ],

        [
            InlineKeyboardButton(text="Диагнозы", callback_data=str(DIAGNOZES)),
            InlineKeyboardButton(text="Дата обращения", callback_data=str(DATE_OF_APPLICATION)),
            InlineKeyboardButton(text="Как узнали о нас", callback_data=str(HOW_FIND_US)),
        ],

        [
            InlineKeyboardButton(text="В каком фонде сейчас", callback_data=str(WHICH_FOND)),
            InlineKeyboardButton(text="Какие фонды помогали", callback_data=str(WHICH_FOND_WAS_PREVIOUSLY)),
        ],
    ]

    FLAGS_OBJ.changing_edit_mode_first(True)
    keyboard = InlineKeyboardMarkup(buttons)

    message = "Выберите пункт, который вы бы хотели изменить."

    await query.edit_message_text(text=message, reply_markup=keyboard)


    return EDIT_USER_DATES


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text("До свидания!")
    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в меню выбора программ."""
    await update.callback_query.answer()
    clean_dictionary(context=context.user_data)
    await application_to_the_fond(update, context)


async def end_second_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в меню вступления в программу."""
    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя
    save_values = ["Программа фонда"]
    clean_dictionary(context=context.user_data, save_values=save_values)

    # Значит, что мы уже дошли до сюдого. Нужно для корректировки вывода в join_or_not_to_programm
    FLAGS_OBJ.changing_edit_mode_first(True)

    buttons = [
        [
            InlineKeyboardButton(text="Продолжить", callback_data=str(SAY_YES)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(text=MSG_PRESS_NEXT_BUTTON, reply_markup=keyboard)

    return QUESTION_THIRD_MENU


