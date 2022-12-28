from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from .menu import start
from core.logger import logger


(
    SELECTING_CHAT,
    CHAT,
    CHAT_BABY,
    CHAT_CHILD,
    SHUNTATA,
    RETINOPATIA,
    GRANDMOTHERS,
    CRY,
    ANGELS,
    RETINOPATIA_4_5,
    PROBLEMS,
    TELECRAM_CHAT,
) = map(chr, range(9, 21))

(
    PARENTS_SURNAME,
    TELEPHONE_NUMBER,
    BABY_SURNAME,
    DATE_OF_BIRTH,
    PLACE_OF_BIRTH,
    TERM_OF_BIRTH,
    WEIGHT,
    HEIGHT,
) = map(chr, range(21, 29))
TYPING = map(chr, range(30, 31))

STOPPING, SHOWING = map(chr, range(31, 33))
END = ConversationHandler.END
(START_OVER, CURRENT_CHAT) = map(chr, range(19, 21))


async def select_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Выбрать чат"""
    buttons_chat = [
        [
            InlineKeyboardButton(
                text="Дети, рожде‌нные раньше срока (до 1,5)",
                callback_data=str(CHAT_BABY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Дети, рожде‌нные раньше срока (от 1,5)",
                callback_data=str(CHAT_CHILD),
            )
        ],
        [
            InlineKeyboardButton(
                text="Ретинопатия", callback_data=str(RETINOPATIA)
            )
        ],
        [InlineKeyboardButton(text="Шунтята", callback_data=str(SHUNTATA))],
        [
            InlineKeyboardButton(
                text="Бабушки торопыжек", callback_data=str(GRANDMOTHERS)
            )
        ],
        [
            InlineKeyboardButton(
                text="Отвести душу и поплакать", callback_data=str(CRY)
            )
        ],
        [InlineKeyboardButton(text="Мамы ангелов", callback_data=str(ANGELS))],
        [
            InlineKeyboardButton(
                text="Ретинопатия недоношенных 4-5 стадии",
                callback_data=str(RETINOPATIA_4_5),
            )
        ],
        [
            InlineKeyboardButton(
                text="Дети с офтальмологическими проблемами",
                callback_data=str(PROBLEMS),
            )
        ],
        [
            InlineKeyboardButton(
                text="«Семьи торопыжек» t.me/toropizhki",
                callback_data=str(TELECRAM_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Возврат в главное меню", callback_data=str(END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons_chat)
    if not context.user_data.get(START_OVER):
        context.user_data[CHAT] = {CHAT: update.callback_query.data}
        text = "Выберите чат для вступления:"

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        text = "Мы получили от Вас информацию!"
        await update.message.reply_text(text=text, reply_markup=keyboard)
    context.user_data[START_OVER] = False
    return SELECTING_CHAT


async def end_second_level(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат к главному меню"""
    context.user_data[START_OVER] = True
    await start(update, context)

    return END


async def stop_nested(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Возврат в главное меню"""
    await update.message.reply_text("Возврат к главному меню")

    return STOPPING


async def chat_baby(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.callback_query.answer()
    text = "chat_baby"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_CHAT


async def chat_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "chat_child"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_CHAT


async def rethinopatia(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "rethinopatia"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_CHAT


async def angels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.callback_query.answer()
    text = "angels"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_CHAT


async def grandmothers(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    pass


async def shuntata(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    pass


async def cry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    pass


async def rethinopatia_4_5(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    pass


async def problems(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    pass


async def telegram_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    pass


async def parents_surname(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заполнение анкеты. ФИО Родителя"""
    user = update.message.from_user
    logger.info("ФИО родителя", user.first_name, update.message.text)
    await update.message.reply_text(
        "Ваш телефонный номер или нажмите /skip для выхода"
    )

    return TELEPHONE_NUMBER


async def telephone_number(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заполнение анкеты. Телефонный номер"""
    user = update.message.from_user
    logger.info("Телефонный номер", user.first_name, update.message.text)
    await update.message.reply_text("ФИО ребенка или нажмите /skip для выхода")

    return BABY_SURNAME


async def baby_surname(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заполнение анкеты. ФИО ребенка"""
    user = update.message.from_user
    logger.info("ФИО ребенка", user.first_name, update.message.text)
    await update.message.reply_text(
        "Дата рождения или нажмите /skip для выхода"
    )

    return DATE_OF_BIRTH


async def date_of_birth(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Дата рождения ребенка", user.first_name, update.message.text)
    await update.message.reply_text(
        "Место рождения или нажмите /skip для выхода"
    )

    return PLACE_OF_BIRTH


async def place_of_birth(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Место рождения ребенка", user.first_name, update.message.text)
    await update.message.reply_text(
        "Срок рождения или нажмите /skip для выхода"
    )

    return TERM_OF_BIRTH


async def term_of_birth(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Срок рождения ребенка", user.first_name, update.message.text)
    await update.message.reply_text(
        "Вес при рождении или нажмите /skip для выхода"
    )

    return WEIGHT


async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Вес", user.first_name, update.message.text)
    await update.message.reply_text("Рост или нажмите /skip для выхода")

    return HEIGHT
