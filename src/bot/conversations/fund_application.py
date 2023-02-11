# Логика "Заявка на вступление в фонд" без хендлеров
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from ..flags.flag import Flags
from ..templates import HTML_TEMPLATE_JOIN_FUND
from ..validators import fund_app_validators as validators
from .menu import start
from bot import constants, keys, states
from core.email import bot_send_email_to_curator
from core.logger import logger


END = ConversationHandler.END

FLAGS_OBJ = Flags()


# Подпрограммы
def clean_dictionary(context: dict, save_values=[None]) -> None:
    """Очистка словаря."""
    for key in context:
        if key not in save_values:
            context[key] = ""


# Здесь начинаются обработчики кнопок и ответов на вопросы
async def application_to_the_fund(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод кнопок программ фонда."""

    buttons = [
        [
            InlineKeyboardButton(
                text=constants.PROGRAM_FUND[keys.LOOK_WORLD_PROGRAM][0],
                callback_data=keys.LOOK_WORLD_PROGRAM,
            ),
            InlineKeyboardButton(
                text=constants.PROGRAM_FUND[keys.REABILITATION_PROGRAM][0],
                callback_data=keys.REABILITATION_PROGRAM,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.PROGRAM_FUND[keys.PSIHO_PROGRAM][0],
                callback_data=keys.PSIHO_PROGRAM,
            ),
            InlineKeyboardButton(
                text=constants.PROGRAM_FUND[keys.KIND_LESSONS_PROGRAM][0],
                callback_data=keys.KIND_LESSONS_PROGRAM,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Главное меню", callback_data=keys.MAIN_MENU
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    if FLAGS_OBJ.first_start:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.MSG_FIRST_MENU, reply_markup=keyboard
        )

    else:
        await update.message.reply_text(
            text=constants.MSG_FIRST_MENU, reply_markup=keyboard
        )
        FLAGS_OBJ.changing_first_start(False)

    return states.JOIN_PROGRAM


async def join_or_not_to_program(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    Вывод информации о фонде, а также кнопок:
    Вступить, назад, в главное меню.
    """
    query = update.callback_query
    await query.answer()
    message_about_fund_and_documents = ""

    if not FLAGS_OBJ.edit_mode_first_flag:
        data = update.callback_query.data
        if data in constants.PROGRAM_FUND:
            message_about_fund_and_documents = (
                f"{constants.PROGRAM_FUND[data][0]}\n"
                + f"{constants.PROGRAM_FUND[data][1]}\n"
                + f"{constants.PROGRAM_FUND[data][2]}\n"
            )
            context.user_data["Программа фонда"] = constants.PROGRAM_FUND[
                data
            ][0]
        else:
            context.user_data["Программа фонда"] = constants.ANSWERS_DICT[
                "bad_answer"
            ]

        context.user_data["Programm"] = data

    else:
        dates_about_fund = constants.PROGRAM_FUND[
            context.user_data["Programm"]
        ]
        message_about_fund_and_documents = (
            f"{dates_about_fund[0]}\n"
            + f"{dates_about_fund[1]}\n"
            + f"{dates_about_fund[2]}\n"
        )

        FLAGS_OBJ.changing_edit_mode_first(False)

    buttons = [
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["join"],
                callback_data=keys.JOIN_BUTTON,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["back"], callback_data=str(END)
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["main_menu"],
                callback_data=keys.MAIN_MENU,
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(
        text=message_about_fund_and_documents + constants.MSG_SECOND_MENU,
        reply_markup=keyboard,
    )

    return states.JOIN_PROGRAM


async def asking_fio_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение фамилии мамы."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["fio_mother"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.FIO_MOTHER

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["fio_mother"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.FIO_MOTHER

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=constants.QUESTIONS_DICT["fio_mother"])

    return states.FIO_MOTHER


async def asking_phone_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение телефона мамы."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["phone_number"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.PHONE

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["phone_number"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.PHONE

    fio = update.message.text

    if not validators.checking_not_digits(fio):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_fio_mother"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)

        return states.RETURN_MOTHER_FIO

    context.user_data["ФИО мамы"] = fio.title()
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constants.QUESTIONS_DICT["phone_number"]
    )

    return states.PHONE


async def asking_email_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение email мамы."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(text=constants.QUESTIONS_DICT["email"])
        FLAGS_OBJ.changing_bad_request(False)
        return states.EMAIL

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constants.QUESTIONS_DICT["email"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.EMAIL

    phone_number = update.message.text

    if not validators.checking_phone_number(phone_number):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_phone_number"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.FIO_MOTHER

    context.user_data["Телефон"] = phone_number
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["email"])

    return states.EMAIL


async def asking_fio_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение ФИО ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["fio_child"]
        )
        FLAGS_OBJ.changing_bad_request(False)

        return states.FIO_CHILD

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["fio_child"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.FIO_CHILD

    email_mother = update.message.text
    if not validators.checking_email(email_mother):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_email"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)

        return states.PHONE

    context.user_data["Email"] = email_mother

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["fio_child"])

    return states.FIO_CHILD


async def asking_how_many_people_in_family(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение количества членов семьи."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["how_many_people"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.HOW_MANY_PEOPLE

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["how_many_people"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.HOW_MANY_PEOPLE

    fio_child = update.message.text

    if not validators.checking_not_digits(fio_child):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_child_fio"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.EMAIL

    context.user_data["ФИО ребёнка"] = fio_child.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constants.QUESTIONS_DICT["how_many_people"]
    )

    return states.HOW_MANY_PEOPLE


async def asking_city(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение города проживания."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(text=constants.QUESTIONS_DICT["city"])
        FLAGS_OBJ.changing_bad_request(False)
        return states.CITY

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constants.QUESTIONS_DICT["city"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.CITY

    how_many_people = update.message.text

    if not validators.checking_count_people_in_family(how_many_people):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_people_in_family"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.FIO_CHILD

    context.user_data["Сколько членов семьи"] = how_many_people
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["city"])

    return states.CITY


async def asking_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение адреса проживания."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["address"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.ADDRESS

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constants.QUESTIONS_DICT["address"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.ADDRESS

    city = update.message.text

    if not validators.checking_not_digits(city):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_city"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.HOW_MANY_PEOPLE

    context.user_data["Город"] = city.title()
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["address"])

    return states.ADDRESS


async def asking_child_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение дня рождения ребенка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["birthday"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.BIRTHDAY

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["birthday"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.BIRTHDAY

    address = update.message.text

    context.user_data["Адрес"] = address.title()
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["birthday"])

    return states.BIRTHDAY


async def asking_place_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение места рождения ребенка."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["place_birth"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.PLACE_BIRTH

    child_birthday = update.message.text

    if not validators.checking_birthday(child_birthday):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_birthday"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.ADDRESS

    context.user_data["Дата рождения ребёнка"] = child_birthday

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constants.QUESTIONS_DICT["place_birth"]
    )

    return states.PLACE_BIRTH


async def asking_birth_date(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение срока рождения ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["birth_date"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.BIRTH_DATE

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["birth_date"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.BIRTH_DATE

    place_birth = update.message.text

    context.user_data["Место рождения ребёнка"] = place_birth.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constants.QUESTIONS_DICT["birth_date"]
    )

    return states.BIRTH_DATE


async def asking_child_weight(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение веса ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["weight"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.WEIGHT

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constants.QUESTIONS_DICT["weight"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.WEIGHT

    birth_date = update.message.text

    if not validators.checking_count_people_in_family(birth_date):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_birth_date"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.PLACE_BIRTH

    context.user_data["Срок рождения ребёнка"] = birth_date

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["weight"])

    return states.WEIGHT


async def asking_child_height(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение роста ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["height"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.HEIGHT

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constants.QUESTIONS_DICT["height"])
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.HEIGHT

    child_weight = update.message.text

    if not validators.checking_weight_and_height(child_weight):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_weight"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.BIRTH_DATE

    context.user_data["Вес"] = child_weight

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["height"])

    return states.HEIGHT


async def asking_child_diagnosis(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение диагнозов ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            text=constants.QUESTIONS_DICT["diagnosis"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return states.DIAGNOSIS

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["diagnosis"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.DIAGNOSIS

    child_height = update.message.text

    if not validators.checking_weight_and_height(child_height):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_height"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.WEIGHT

    context.user_data["Рост"] = child_height

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["diagnosis"])

    return states.DIAGNOSIS


async def asking_how_found_us(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение информации о том, как нашли фонд."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constants.QUESTIONS_DICT["how_found_fund"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.HOW_FOUND

    diagnosis = update.message.text
    if not validators.checking_not_digits(diagnosis):
        await update.message.reply_text(
            text=constants.ANSWERS_DICT["bad_diagnosis"],
            reply_markup=constants.MARKUP_FIX,
        )
        FLAGS_OBJ.changing_bad_request(True)
        return states.HEIGHT

    context.user_data["Диагнозы"] = diagnosis.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constants.QUESTIONS_DICT["how_found_fund"]
    )

    return states.HOW_FOUND


async def asking_which_fund_now(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    Получение информации о том, состоят ли ещё в
    каком-либо фонде в данный момент.
    """

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["fund_now"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.WHICH_FUND

    how_found_us = update.message.text

    context.user_data["Как узнали о нас"] = how_found_us.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constants.QUESTIONS_DICT["fund_now"])

    return states.WHICH_FUND


async def asking_which_funds_helped(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение информации о том, какие фонды помогали раньше."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constants.QUESTIONS_DICT["which_fund"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return states.WHICH_FUND_WAS_PREVIOUSLY

    which_fund_now = update.message.text

    context.user_data["В фонде сейчас"] = which_fund_now.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constants.QUESTIONS_DICT["which_fund"]
    )

    return states.WHICH_FUND_WAS_PREVIOUSLY


async def show_user_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение пользователю полученной информации."""

    which_funds_helped = update.message.text

    context.user_data["Фонды помогали"] = which_funds_helped.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    for key, data in context.user_data.items():
        if key not in constants.SECRET_KEY:
            await update.message.reply_text(text=f"{key}: {data}")

    return await send_or_change_data(update, context)


async def show_user_edit_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение пользователю обновленной
    информации после редактирования."""

    for key, data in context.user_data.items():
        if key not in constants.SECRET_KEY:
            await update.message.reply_text(text=f"{key}: {data}")

    return await send_or_change_data(update, context)


async def send_or_change_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Меню с выбором дальнейших действий:
    - Отправить данные куратору
    - Изменить данные
    - Назад
    """

    buttons = [
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["confirm_and_send"],
                callback_data=keys.CONFIRM_AND_SEND,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["change_data"],
                callback_data=keys.CHANGE_DATA,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["back"],
                callback_data=keys.END_SECOND_LEVEL,
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text=constants.MSG_THIRD_MENU, reply_markup=keyboard
    )

    return states.EDIT_USER_DATА


async def send_message_to_curator(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка сообщения куратору с данными.
    Пока без фотографии/сканов."""
    query = update.callback_query
    await query.answer()
    date_now = date.today()
    date_of_application = f"{date_now.day}.{date_now.month}.{date_now.year}"
    context.user_data["Дата обращения"] = date_of_application

    try:
        html_from_user = HTML_TEMPLATE_JOIN_FUND.substitute(
            mother_fio=context.user_data["ФИО мамы"],
            programm=context.user_data["Программа фонда"],
            mother_phone=context.user_data["Телефон"],
            mother_email=context.user_data["Email"],
            child_fio=context.user_data["ФИО ребёнка"],
            how_many_people=context.user_data["Сколько членов семьи"],
            city=context.user_data["Город"],
            adress=context.user_data["Адрес"],
            child_birthday=context.user_data["Дата рождения ребёнка"],
            place_birth=context.user_data["Место рождения ребёнка"],
            birth_date=context.user_data["Срок рождения ребёнка"],
            weight=context.user_data["Вес"],
            height=context.user_data["Рост"],
            dizgnozes=context.user_data["Диагнозы"],
            date_aplication=context.user_data["Дата обращения"],
            how_about_us=context.user_data["Как узнали о нас"],
            fund_now=context.user_data["В фонде сейчас"],
            fund_early=context.user_data["Фонды помогали"],
        )

        bot_send_email_to_curator(constants.SUBJECT, html_from_user)
    except Exception as ex:
        logger.error(ex)
        html_from_user = HTML_TEMPLATE_JOIN_FUND.substitute(error=ex)
        bot_send_email_to_curator(constants.SUBJECT_ERROR, html_from_user)
        logger.info("Ошибка отправлена куратору!")

    documents = "Вам сообщит куратор."

    if context.user_data["Programm"] in constants.PROGRAM_FUND:
        documents = constants.PROGRAM_FUND[context.user_data["Programm"]][2]

    button = [
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["back_to_menu"],
                callback_data=str(END),
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(button)

    await query.edit_message_text(
        text=constants.MESSAGE_SUCCESSFUL_DEPARTURE_TO_CURATOR + documents,
        reply_markup=keyboard,
    )

    return states.END_FIRST_LEVEL


async def change_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Изменение данных пользователя через кнопки."""
    query = update.callback_query

    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["fio_mother"],
                callback_data=keys.FIO_MOTHER,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["phone_number"],
                callback_data=keys.PHONE,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["email"],
                callback_data=keys.EMAIL,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["fio_child"],
                callback_data=keys.FIO_CHILD,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["how_many_people"],
                callback_data=keys.HOW_MANY_PEOPLE,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["city"],
                callback_data=keys.CITY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["address"],
                callback_data=keys.ADDRESS,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["birthday"],
                callback_data=keys.BIRTHDAY,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["place_birth"],
                callback_data=keys.PLACE_BIRTH,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["birth_date"],
                callback_data=keys.BIRTH_DATE,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["weight"],
                callback_data=keys.WEIGHT,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["height"],
                callback_data=keys.HEIGHT,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["diagnosis"],
                callback_data=keys.DIAGNOSIS,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["how_found_fund"],
                callback_data=keys.HOW_FOUND,
            ),
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["which_fund"],
                callback_data=keys.WHICH_FUND,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constants.BUTTONS_TEXT["fund_now"],
                callback_data=keys.WHICH_FUND_WAS_PREVIOUSLY,
            ),
        ],
    ]

    FLAGS_OBJ.changing_edit_mode_first(True)
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=constants.MSG_EDIT, reply_markup=keyboard
    )

    return states.EDIT_USER_DATА


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в меню выбора программ."""
    await update.callback_query.answer()
    clean_dictionary(context=context.user_data)
    await application_to_the_fund(update, context)


async def end_second_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат в меню вступления в программу."""
    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя с сохранением выбранной программы
    save_values = ["Programm", "Программа фонда"]
    clean_dictionary(context=context.user_data, save_values=save_values)

    # Нужно для корректировки вывода в join_or_not_to_programm
    FLAGS_OBJ.changing_edit_mode_first(True)

    await join_or_not_to_program(update, context)
    return states.END_FIRST_LEVEL


async def return_main_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат в главное меню."""
    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя
    clean_dictionary(context=context.user_data)

    context.user_data[keys.START_OVER] = True
    FLAGS_OBJ.changing_first_start(True)

    await start(update, context)
    return states.END_MAIN_MENU


async def stop_nested(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    clean_dictionary(context=context.user_data)

    await update.message.reply_text(text=constants.MSG_GOODBYE)
    return states.STOPPING
