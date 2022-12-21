import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)



# Выбор главного меню
SELECTING_ACTION, CHAT, APPLICATION, VOLUNTEER, TALK, DONATION, EVENTS, QUESTION, ABOUT = map(chr, range(9))
# Меню второго уровня в чатах
SELECTING_CHAT, CHAT_BABY, CHAT_CHILD, SHUNTATA, RETINOPATIA, GRANDMOTHERS, CRY = map(chr, range(9, 15))
# Обмен информацией
SELECTING_FEATURE, TYPING = map(chr, range(15, 17))
# Общие функции
STOPPING, SHOWING = map(chr, range(17, 19))
# Выход for ConversationHandler.END
END = ConversationHandler.END
#Константы
(START_OVER,) = map(chr, range(19, 20))

# Главное меню - возврат выбора
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Главное меню бота. Выбор пункта меню"""
    text = (
        'Привет! Я бот-помощник фонда помощи '
        'недоношенным детям и их семьям "Провидение".\n '
        'Мы спасаем зрение недоношенным детям.\n'
        'Я помогу Вам как получить, так и оказать помощь!\n'
        'Выберите пункт меню: \n'
    )
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

    await update.message.reply_text(text=text, reply_markup=keyboard)


    return SELECTING_ACTION




async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение разговора"""
    await update.message.reply_html(
        text='Будем рады видеть Вас на нашем сайте! \n <b><a>https://fond-providenie.ru</a></b> ')

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение из InlineKeyboardButton."""
    await update.callback_query.answer()

    text = 'Будем рады видеть Вас на нашем сайте! \n https://fond-providenie.ru'
    await update.callback_query.edit_message_text(text=text)

    return END


# Второй уровень чаты
async def select_level_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Выбор чата."""
    text = "У нас есть такие чаты:"
    buttons = [
        [InlineKeyboardButton(text="Чат для родителей детей, рожде‌нных раньше срока (до 1,5 лет)", callback_data=str(CHAT_BABY))],
        [InlineKeyboardButton(text="Чат для родителей детей, рожде‌нных раньше срока (от 1,5 лет и старше)", callback_data=str(CHAT_CHILD))],
        [InlineKeyboardButton(text="Ретинопатия", callback_data=str(RETINOPATIA))],
        [InlineKeyboardButton(text="Шунтята", callback_data=str(SHUNTATA))],
        [InlineKeyboardButton(text="Бабушки торопыжек", callback_data=str(GRANDMOTHERS))],
        [InlineKeyboardButton(text="Отвести душу и поплакать", callback_data=str(CRY))],
        [InlineKeyboardButton(text="Возврат в главное меню", callback_data=str(END))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_CHAT


async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в главное меню"""
    context.user_data[START_OVER] = True
    await start(update, context)

    return END




async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Полный выход из бота"""
    await update.message.reply_text("Okay, bye.")

    return STOPPING


async def entry_chat():
    pass

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



    # Второй уровень меню в чатах

    # top level ConversationHandler (selecting action)
selection_handlers = [
    CallbackQueryHandler(entry_chat, pattern="^" + str(CHAT) + "$"),
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



