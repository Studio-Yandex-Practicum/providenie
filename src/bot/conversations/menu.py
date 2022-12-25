import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



# Выбор главного меню
SELECTING_ACTION, CHAT, APPLICATION, VOLUNTEER, TALK, DONATION, EVENTS, QUESTION, ABOUT = map(chr, range(9))
# Меню второго уровня в чатах
SELECTING_CHAT, CHAT_BABY, CHAT_CHILD, SHUNTATA, RETINOPATIA, GRANDMOTHERS, CRY, ANGELS, RETINOPATIA_4_5, PROBLEMS, TELECRAM_CHAT = map(chr, range(9, 20))
# Обмен информацией
PARENTS_SURNAME, TELEPHONE_NUMBER, BABY_SURNAME, DATE_OF_BIRTH, PLACE_OF_BIRTH, TERM_OF_BIRTH, WEIGHT, HEIGHT = map(chr, range(21, 29))
SELECTING_CHAT, TYPING = map(chr, range(29, 31))
# Общие функции
STOPPING, SHOWING = map(chr, range(31, 33))
# Выход for ConversationHandler.END
END = ConversationHandler.END
#Константы
(START_OVER, CURRENT_CHAT) = map(chr, range(19, 21))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод приветствия."""
    text_start_button = (
        'Привет! Я бот-помощник фонда помощи '
        'недоношенным детям и их семьям "Провидение".\n '
        'Мы спасаем зрение недоношенным детям.\n'
        'Я помогу Вам как получить, так и оказать помощь!\n'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_start_button
    )


# Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Главное меню бота. Выбор пункта меню"""
    text = 'Вы можете выбрать любую программу:'
    buttons = [
        [InlineKeyboardButton(text='Хочу попасть в родительский чат', callback_data=str(CHAT))],
        [InlineKeyboardButton(text='Заявка в фонд', callback_data=str(APPLICATION))],
        [InlineKeyboardButton(text='Хочу стать волонтером', callback_data=str(VOLUNTEER))],
        [InlineKeyboardButton(text='Рассказать о Фонде своим друзьям', callback_data=str(TALK))],
        [InlineKeyboardButton(text='Пожертвование', callback_data=str(DONATION))],
        [InlineKeyboardButton(text='Наши события', callback_data=str(EVENTS)),
         InlineKeyboardButton(text='Задать вопрос', callback_data=str(QUESTION))],
        [InlineKeyboardButton(text='О Фонде', callback_data=str(ABOUT)),
         InlineKeyboardButton(text='Выход', callback_data=str(END))]
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(reply_markup=keyboard)
    else:
        await update.message.reply_text(
            'Я бот-помощник фонда помощи недоношенным детям и их семьям "Провидение". '
        )
        await update.message.reply_text(reply_markup=keyboard, text=text)

    context.user_data[START_OVER] = False

    return SELECTING_ACTION


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение разговора по команде /stop"""
    await update.message.reply_html(
        text='Будем рады видеть Вас на нашем сайте! \n <b><a>https://fond-providenie.ru</a></b> ')
    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение по команде из меню"""
    await update.callback_query.answer()
    text = 'Будем рады видеть Вас на нашем сайте! \n https://fond-providenie.ru'
    await update.callback_query.edit_message_text(text=text)

    return END


async def select_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Выбрать чат"""
    buttons_chat = [
        [InlineKeyboardButton(text='Дети, рожде‌нные раньше срока (до 1,5)',
                              callback_data=str(CHAT_BABY))],
        [InlineKeyboardButton(text='Дети, рожде‌нные раньше срока (от 1,5)',
                              callback_data=str(CHAT_CHILD))],
        [InlineKeyboardButton(text='Ретинопатия', callback_data=str(RETINOPATIA))],
        [InlineKeyboardButton(text='Шунтята', callback_data=str(SHUNTATA))],
        [InlineKeyboardButton(text='Бабушки торопыжек', callback_data=str(GRANDMOTHERS))],
        [InlineKeyboardButton(text='Отвести душу и поплакать', callback_data=str(CRY))],
        [InlineKeyboardButton(text='Мамы ангелов', callback_data=str(ANGELS))],
        [InlineKeyboardButton(text='Ретинопатия недоношенных 4-5 стадии', callback_data=str(RETINOPATIA_4_5))],
        [InlineKeyboardButton(text='Дети с офтальмологическими проблемами', callback_data=str(PROBLEMS))],
        [InlineKeyboardButton(text='«Семьи торопыжек» t.me/toropizhki',
                              callback_data=str(TELECRAM_CHAT))],
        [InlineKeyboardButton(text="Возврат в главное меню", callback_data=str(END))]

    ]
    keyboard = InlineKeyboardMarkup(buttons_chat)
    if not context.user_data.get(START_OVER):
        context.user_data[CHAT] = {CHAT: update.callback_query.data}
        text = "Выберите чат для вступления:"

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        text = "Мы получили от Вас информацию!"
        await update.message.reply_text(text=text, reply_markup=keyboard)
    user_data = context.user_data
    context.user_data[START_OVER] = False
    return PARENTS_SURNAME



async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Возврат в главное меню"""
    await update.message.reply_text("Возврат к главному меню")

    return STOPPING


async def parents_surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. ФИО Родителя"""
    user = update.message.from_user
    logger.info("ФИО родителя", user.first_name, update.message.text)
    await update.message.reply_text("Ваш телефонный номер или нажмите /skip для выхода")

    return TELEPHONE_NUMBER


async def telephone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. Телефонный номер"""
    user = update.message.from_user
    logger.info("Телефонный номер", user.first_name, update.message.text)
    await update.message.reply_text("ФИО ребенка или нажмите /skip для выхода")

    return BABY_SURNAME

async def baby_surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. ФИО ребенка"""
    user = update.message.from_user
    logger.info("ФИО ребенка", user.first_name, update.message.text)
    await update.message.reply_text("Дата рождения или нажмите /skip для выхода")

    return DATE_OF_BIRTH

async def date_of_birth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Дата рождения ребенка", user.first_name, update.message.text)
    await update.message.reply_text("Место рождения или нажмите /skip для выхода")

    return PLACE_OF_BIRTH

async def place_of_birth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Место рождения ребенка", user.first_name, update.message.text)
    await update.message.reply_text("Срок рождения или нажмите /skip для выхода")

    return TERM_OF_BIRTH

async def term_of_birth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Срок рождения ребенка", user.first_name, update.message.text)
    await update.message.reply_text("Вес при рождении или нажмите /skip для выхода")

    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заполнение анкеты. Дата рождения ребенка"""
    user = update.message.from_user
    logger.info("Вес", user.first_name, update.message.text)
    await update.message.reply_text("Рост или нажмите /skip для выхода")

    return HEIGHT

async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в главное меню"""
    context.user_data[START_OVER] = True
    await start(update, context)

    return END



async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Выход из бота из подменю"""
    await update.message.reply_text('Будем рады видеть Вас на нашем сайте! \n '
                                    'https://fond-providenie.ru')

    return STOPPING



async def application():
    pass

async def become_volunteer():
    pass

async def talk_friends():
    pass

async def give_donation():
    pass

async def get_events():
    pass

async def ask_question():
    pass

async def get_about_fond():
    pass

description_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        select_chat, pattern="^" + str(CHAT_BABY) + "$|^" + str(CHAT_CHILD) + "$|"
        "^" + str(RETINOPATIA) + "$|^" + str(SHUNTATA) + "$|^" + str(GRANDMOTHERS) + "$|"
        "^" + str(CRY) + "$|^" + str(ANGELS) + "$|^" + str(RETINOPATIA_4_5) + "$|"
        "^" + str(PROBLEMS) + "$|^" + str(TELECRAM_CHAT) + "$")],
    states={
        PARENTS_SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, parents_surname)],
        TELEPHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, telephone_number)],
        BABY_SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, baby_surname)]},
    fallbacks=[
        CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
        CommandHandler("stop", stop_nested)],
    map_to_parent={
         END: SELECTING_CHAT,
         STOPPING: STOPPING,
         },
)


selection_handlers = [
    description_conv,
    CallbackQueryHandler(select_chat, pattern="^" + str(CHAT) + "$"),
    CallbackQueryHandler(application, pattern="^" + str(APPLICATION) + "$"),
    CallbackQueryHandler(become_volunteer, pattern="^" + str(VOLUNTEER) + "$"),
    CallbackQueryHandler(talk_friends, pattern="^" + str(TALK) + "$"),
    CallbackQueryHandler(give_donation, pattern="^" + str(DONATION) + "$"),
    CallbackQueryHandler(get_events, pattern="^" + str(EVENTS) + "$"),
    CallbackQueryHandler(ask_question, pattern="^" + str(QUESTION) + "$"),
    CallbackQueryHandler(get_about_fond, pattern="^" + str(ABOUT) + "$"),
    CallbackQueryHandler(end, pattern="^" + str(END) + "$")
]



conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
        SELECTING_ACTION: selection_handlers,
        STOPPING: [CommandHandler("start", start)],
        },
    fallbacks=[CommandHandler("end", end)],
    )


application = Application.builder().token('5648577099:AAFPdt2Q3R4LGUfDkdLsaa_cM_EVDQEz0A0').build()
application.add_handler(conv_handler)



    # Run the bot until the user presses Ctrl-C
application.run_polling()
