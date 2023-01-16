# Логика "Заявка на вступление в фонд" без хендлеров
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler

from bot import states
from ..constans import fund_app_constans as constans
from core.email import bot_send_email_to_curator
from core.logger import logger
from ..flags.flag import Flags
from ..templates import HTML_TEMPLATE_JOIN_FOND
from ..validators import fund_app_validators as validators


END = ConversationHandler.END

FLAGS_OBJ = Flags()


# Подпрограммы
def clean_dictionary(context, save_values=[None]) -> None:
    """Очистка словаря."""
    for key in context:
        if key not in save_values:
            context[key] = ""


# Здесь начинаются обработчики кнопок и ответов на вопросы
async def application_to_the_fond(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод кнопок программ фонда."""

    buttons = [
        [
            InlineKeyboardButton(
                text="Смотри на мир",
                callback_data=str(constans.LOOK_WORLD_PROGRAMM)
            ),
            InlineKeyboardButton(
                text="Реабилитация",
                callback_data=str(constans.REABILITATION_PROGRAMM)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Психологическая помощь",
                callback_data=str(constans.PSIHO_PROGRAMM)
            ),
            InlineKeyboardButton(
                text="Добрые уроки",
                callback_data=str(constans.KIND_ARMS_PROGRAMM)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Главное меню",
                callback_data=str(constans.MAIN_MENU)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    if FLAGS_OBJ.first_start:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.MSG_FIRST_MENU,
            reply_markup=keyboard
        )

    else:
        await update.message.reply_text(
            text=constans.MSG_FIRST_MENU,
            reply_markup=keyboard
        )
        FLAGS_OBJ.changing_first_start(False)

    return constans.CHOICE_PROGRAMM


async def join_or_not_to_programm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    Вывод информации о фонде, а также кнопок:
    Вступить, назад, в главное меню.
    """
    query = update.callback_query
    await query.answer()
    message_about_fond_and_documations = ''

    if not FLAGS_OBJ.edit_mode_first_flag:
        data = update.callback_query.data
        if data in constans.PROGRAMM_FOND:
            message_about_fond_and_documations = (
                f"{constans.PROGRAMM_FOND[data][0]}\n" +
                f"{constans.PROGRAMM_FOND[data][1]}\n" +
                f"{constans.PROGRAMM_FOND[data][2]}\n"
            )
            context.user_data[
                "Программа фонда"
            ] = constans.PROGRAMM_FOND[data][0]
        else:
            context.user_data[
                "Программа фонда"
            ] = constans.ANSWERS_DICT["bad_answer"]

    else:
        dates_about_fond = constans.PROGRAMM_FOND[
            constans.ALLIAS_DICT[context.user_data["Программа фонда"]]
        ]
        message_about_fond_and_documations = (
            f"{dates_about_fond[0]}\n" +
            f"{dates_about_fond[1]}\n" +
            f"{dates_about_fond[2]}\n"
        )

        FLAGS_OBJ.changing_edit_mode_first(False)

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить",
                callback_data=str(constans.JOIN_BUTTON)
            ),
            InlineKeyboardButton(
                text="Назад",
                callback_data=str(END)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Главное меню",
                callback_data=str(constans.MAIN_MENU)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(
        text=message_about_fond_and_documations +
        constans.MSG_SECOND_MENU,
        reply_markup=keyboard,
    )

    return constans.JOIN_TO_PROGRAMM


async def go_second_level(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Переход на второй уровень."""
    query = update.callback_query
    await query.edit_message_text(
        text=constans.MSG_PRESS_ANY_BUTTON,
    )

    return constans.GO_SECOND_LEVEL


async def asking_fio_mother(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение фамилии мамы."""
    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["fio_mother"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.FIO_MOTHER

    await update.message.reply_text(constans.QUESTIONS_DICT["fio_mother"])

    return constans.FIO_MOTHER


async def asking_phone_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение телефона мамы."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["phone_number"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.PHONE

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["phone_number"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.PHONE

    fio = update.message.text

    if not validators.checking_not_digits(fio):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_fio_mother"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)

        return constans.RETURN_MOTHER_FIO

    context.user_data["ФИО мамы"] = fio.title()
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )

        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["phone_number"]
    )

    return constans.PHONE


async def asking_email_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение email мамы."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["email"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.EMAIL

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["email"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.EMAIL

    phone_number = update.message.text

    if not validators.checking_not_phone_number(phone_number):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_phone_number"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.FIO_MOTHER

    context.user_data["Телефон"] = phone_number
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )

        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["email"]
    )

    return constans.EMAIL


async def asking_fio_child(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение ФИО ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["fio_child"]
        )
        FLAGS_OBJ.changing_bad_request(False)

        return constans.FIO_CHILD

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["fio_child"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.FIO_CHILD

    email_mother = update.message.text
    if not validators.checking_email(email_mother):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_email"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)

        return constans.PHONE

    context.user_data["Email"] = email_mother

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["fio_child"]
    )

    return constans.FIO_CHILD


async def asking_how_many_people_in_famaly(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение количества членов семьи."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["how_many_people"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.HOW_MANY_PEOPLE

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["how_many_people"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.HOW_MANY_PEOPLE

    fio_child = update.message.text

    if not validators.checking_not_digits(fio_child):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_child_fio"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.EMAIL

    context.user_data["ФИО ребёнка"] = fio_child.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["how_many_people"]
    )

    return constans.HOW_MANY_PEOPLE


async def asking_city(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение города проживания."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["city"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.CITY

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["city"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.CITY

    how_many_piople = update.message.text

    if not validators.checking_number_people_in_family(
        how_many_piople
    ):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_people_in_famaly"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.FIO_CHILD

    context.user_data["Сколько членов семьи"] = how_many_piople
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["city"]
    )

    return constans.CITY


async def asking_address(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение адреса проживания."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["address"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.ADDRESS

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["address"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.ADDRESS

    city = update.message.text

    if not validators.checking_not_digits(city):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_city"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.HOW_MANY_PEOPLE

    context.user_data["Город"] = city.title()
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["address"]
    )

    return constans.ADDRESS


async def asking_child_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение дня рождения ребенка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["date_birth"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.DATE_BIRTH

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["date_birth"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.DATE_BIRTH

    address = update.message.text

    context.user_data["Адрес"] = address.title()
    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["date_birth"]
    )

    return constans.DATE_BIRTH


async def asking_place_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение места рождения ребенка."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["place_birth"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.PLACE_BIRTH

    child_birthsday = update.message.text

    if not validators.checking_date_birth(child_birthsday):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_date_birth"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.ADDRESS

    context.user_data["Дата рождения ребёнка"] = child_birthsday

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["place_birth"]
    )

    return constans.PLACE_BIRTH


async def asking_spacing(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение срока рождения ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["spacing"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.SPACING

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["spacing"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.SPACING

    place_birth = update.message.text

    context.user_data["Место рождения ребёнка"] = place_birth.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["spacing"]
    )

    return constans.SPACING


async def asking_child_weight(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение веса ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["weight"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.WEIGHT

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["weight"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.WEIGHT

    spacing = update.message.text

    if not validators.checking_number_people_in_family(spacing):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_spacing"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.PLACE_BIRTH

    context.user_data["Срок рождения ребёнка"] = spacing

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["weight"]
    )

    return constans.WEIGHT


async def asking_child_height(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение роста ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["height"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.HEIGHT

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["height"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.HEIGHT

    child_weight = update.message.text

    if not validators.checking_weight_and_height(child_weight):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_weight"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.SPACING

    context.user_data["Вес"] = child_weight

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["height"]
    )

    return constans.HEIGHT


async def asking_child_diagnosis(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение диагнозов ребёнка."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["diagnosis"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.DIAGNOSIS

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["diagnosis"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.DIAGNOSIS

    child_height = update.message.text

    if not validators.checking_weight_and_height(child_height):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_height"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.WEIGHT

    context.user_data["Рост"] = child_height

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["diagnosis"]
    )

    return constans.DIAGNOSIS


async def asking_date_of_application(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение обращения в фонд."""
    if FLAGS_OBJ.bad_request:
        await update.message.reply_text(
            constans.QUESTIONS_DICT["date_aplication"]
        )
        FLAGS_OBJ.changing_bad_request(False)
        return constans.DATE_OF_APPLICATION

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["date_aplication"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.DATE_OF_APPLICATION

    diagnosis = update.message.text

    if not validators.checking_not_digits(diagnosis):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_diagnosis"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.HEIGHT

    context.user_data["Диагнозы"] = diagnosis.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["date_aplication"]
    )

    return constans.DATE_OF_APPLICATION


async def asking_how_find_us(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение информации о том, как нашли фонд."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["how_find_fond"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.HOW_FIND_US

    date_of_application = update.message.text

    if not validators.checking_date_birth(date_of_application):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_date_application"],
            reply_markup=constans.MARKUP_FIX
        )
        FLAGS_OBJ.changing_bad_request(True)
        return constans.DIAGNOSIS

    context.user_data["Дата обращения"] = date_of_application

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["how_find_fond"]
    )

    return constans.HOW_FIND_US


async def asking_which_fond_now(
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
            constans.QUESTIONS_DICT["fond_now"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.WHICH_FOND

    how_find_us = update.message.text

    context.user_data["Как узнали о нас"] = how_find_us.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["fond_now"]
    )

    return constans.WHICH_FOND


async def asking_which_fonds_halped(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение информации о том, какие фонды помогали раньше."""

    if FLAGS_OBJ.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["which_fond"]
        )
        FLAGS_OBJ.changing_edit_mode_first(False)
        FLAGS_OBJ.changing_edit_mode_second(True)
        return constans.WHICH_FOND_WAS_PREVIOUSLY

    which_fond_now = update.message.text

    context.user_data["В фонде сейчас"] = which_fond_now.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    await update.message.reply_text(
        constans.QUESTIONS_DICT["which_fond"]
    )

    return constans.WHICH_FOND_WAS_PREVIOUSLY


async def show_user_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение пользователю пролученной информации."""

    which_fonds_halped = update.message.text

    context.user_data["Фонды помогали"] = which_fonds_halped.title()

    if FLAGS_OBJ.edit_mode_second_flag:
        FLAGS_OBJ.changing_edit_mode_second(False)
        await update.message.reply_text(
            constans.MSG_PRESS_NEXT_BUTTON,
            reply_markup=constans.MARKUP_NEXT,
        )
        return constans.SHOW_EDIT_INFORMATIONS

    for key, data in context.user_data.items():
        if key != 'd':
            await update.message.reply_text(f"{key}: {data}")

    await update.message.reply_text(
        constans.MSG_PRESS_NEXT_BUTTON,
        reply_markup=constans.MARKUP_NEXT,
    )

    return constans.SHOW_INFORMATION


async def show_user_edit_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение пользователю обновленной
    информации после редактирования."""

    for key, data in context.user_data.items():
        if key != 'd':
            await update.message.reply_text(f"{key}: {data}")

    await update.message.reply_text(
        constans.MSG_PRESS_NEXT_BUTTON,
        reply_markup=constans.MARKUP_NEXT,
    )

    return constans.SHOW_INFORMATION


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
                text="Подтвердить и отправить",
                callback_data=str(constans.CONFIRM_AND_SEND)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Изменить данные",
                callback_data=str(constans.CHANGE_DATA)
            ),
            InlineKeyboardButton(
                text="Назад",
                callback_data=str(constans.END_SECOND_LEVEL)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text=constans.MSG_THIRD_MENU,
        reply_markup=keyboard)

    return constans.SEND_CHANGE_END


async def send_message_to_curator(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка сообщения куратору с данными.
    Пока без фотографии/сканов."""

    query = update.callback_query
    await query.answer()
    try:
        html_from_user = HTML_TEMPLATE_JOIN_FOND.substitute(
            mother_fio=context.user_data["ФИО мамы"],
            programm=context.user_data["Программа фонда"],
            mother_phone=context.user_data["Телефон"],
            mother_email=context.user_data["Email"],
            child_fio=context.user_data["ФИО ребёнка"],
            how_many_people=context.user_data["Сколько членов семьи"],
            city=context.user_data["Город"],
            adress=context.user_data["Адрес"],
            child_date_birth=context.user_data["Дата рождения ребёнка"],
            place_birth=context.user_data["Место рождения ребёнка"],
            spacing=context.user_data["Срок рождения ребёнка"],
            weight=context.user_data["Вес"],
            height=context.user_data["Рост"],
            dizgnozes=context.user_data["Диагнозы"],
            date_aplication=context.user_data["Дата обращения"],
            how_about_us=context.user_data["Как узнали о нас"],
            fond_now=context.user_data["В фонде сейчас"],
            fond_early=context.user_data["Фонды помогали"],
        )

        bot_send_email_to_curator(constans.SUBJECT, html_from_user)
    except Exception as ex:
        logger.error(ex)
        html_from_user = HTML_TEMPLATE_JOIN_FOND.substitute(error=ex)
        bot_send_email_to_curator(constans.SUBJECT_ERROR, html_from_user)
        logger.info("Ошибка отправлена куратору!")

    documents = "Вам сообщит куратор."

    if context.user_data["Программа фонда"] in constans.ALLIAS_DICT:
        documents = constans.PROGRAMM_FOND[
            constans.ALLIAS_DICT[context.user_data["Программа фонда"]]
        ][2]

    button = [
        [
            InlineKeyboardButton(
                text="Назад в меню",
                callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(button)

    await query.edit_message_text(
        text=constans.MESSAGE_SUCCESSFUL_DEPARTURE_TO_CURATOR +
        documents,
        reply_markup=keyboard
    )

    return constans.MESSAGE_SENT_SUCCESSFULLY


async def change_data(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Изменение данных пользователя через кнопки."""
    query = update.callback_query

    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                text="ФИО мамы",
                callback_data=str(constans.FIO_MOTHER)
            ),
            InlineKeyboardButton(
                text="Телефон",
                callback_data=str(constans.PHONE)
            ),
            InlineKeyboardButton(
                text="Email",
                callback_data=str(constans.EMAIL)
            ),
        ],
        [
            InlineKeyboardButton(
                text="ФИО ребёнка",
                callback_data=str(constans.FIO_CHILD)
            ),
            InlineKeyboardButton(
                text="Количество членов семьи",
                callback_data=str(constans.HOW_MANY_PEOPLE)
            ),
            InlineKeyboardButton(
                text="Город",
                callback_data=str(constans.CITY)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Адрес",
                callback_data=str(constans.ADDRESS)
            ),
            InlineKeyboardButton(
                text="Дата рождения ребёнка",
                callback_data=str(constans.DATE_BIRTH)
            ),
            InlineKeyboardButton(
                text="Место рождения ребёнка",
                callback_data=str(constans.PLACE_BIRTH)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Срок рождения",
                callback_data=str(constans.SPACING)
            ),
            InlineKeyboardButton(
                text="Вес",
                callback_data=str(constans.WEIGHT)
            ),
            InlineKeyboardButton(
                text="Рост",
                callback_data=str(constans.HEIGHT)
            ),
        ],
        [
            InlineKeyboardButton(
                text="Диагнозы",
                callback_data=str(constans.DIAGNOSIS)
            ),
            InlineKeyboardButton(
                text="Дата обращения",
                callback_data=str(constans.DATE_OF_APPLICATION)
            ),
            InlineKeyboardButton(
                text="Как узнали о нас",
                callback_data=str(constans.HOW_FIND_US)
            ),
        ],
        [
            InlineKeyboardButton(
                text="В каком фонде сейчас",
                callback_data=str(constans.WHICH_FOND)
            ),
            InlineKeyboardButton(
                text="Какие фонды помогали",
                callback_data=str(constans.WHICH_FOND_WAS_PREVIOUSLY),
            ),
        ],
    ]

    FLAGS_OBJ.changing_edit_mode_first(True)
    keyboard = InlineKeyboardMarkup(buttons)

    message = "Выберите пункт, который вы бы хотели изменить."

    await query.edit_message_text(text=message, reply_markup=keyboard)

    return constans.EDIT_USER_DATES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в меню выбора программ."""
    await update.callback_query.answer()
    clean_dictionary(context=context.user_data)
    await application_to_the_fond(update, context)


async def end_second_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат в меню вступления в программу."""
    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя
    save_values = ["Программа фонда"]
    clean_dictionary(context=context.user_data, save_values=save_values)

    # Нужно для корректировки вывода в join_or_not_to_programm
    FLAGS_OBJ.changing_edit_mode_first(True)

    buttons = [
        [
            InlineKeyboardButton(
                text="Продолжить",
                callback_data=str(constans.SAY_YES)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=constans.MSG_PRESS_NEXT_BUTTON,
        reply_markup=keyboard
    )

    return constans.QUESTION_THIRD_MENU


async def return_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат в главное меню."""
    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя
    clean_dictionary(context=context.user_data)

    buttons = [
        [
            InlineKeyboardButton(
                text="Продолжить",
                callback_data=str(constans.GO_MAIN_MENU)
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=constans.MSG_PRESS_NEXT_BUTTON,
        reply_markup=keyboard
    )
    context.user_data[states.START_OVER] = True
    FLAGS_OBJ.changing_first_start(True)

    return constans.END_MAIN_MENU


async def stop_nested(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    clean_dictionary(context=context.user_data)

    await update.message.reply_text(
        "До свидания! Будем рады видеть Вас на нашем сайте!\n"
        "https://fond-providenie.ru\n"
        "Нажмите /start для повторного запуска"
    )
    return states.STOPPING
