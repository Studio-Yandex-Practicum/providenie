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
SELECTING_CHAT, TYPING = map(chr, range(20, 22))
# Общие функции
STOPPING, SHOWING = map(chr, range(22, 24))
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
    text = (
        'Вы можете выбрать любую программу! (для выхода просто наберите /stop.)'
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
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(
            'Я бот-помощник фонда помощи недоношенным детям и их семьям "Провидение"'
            'Вы можете выбрать любую программу! (для выхода просто наберите /stop.)'
        )
        await update.message.reply_text(text=text, reply_markup=keyboard)

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
        [InlineKeyboardButton(text="Чат для родителей детей, рожде‌нных раньше срока (до 1,5 лет)",
                              callback_data=str(CHAT_BABY))],
        [InlineKeyboardButton(text="Чат для родителей детей, рожде‌нных раньше срока (от 1,5 лет и старше)",
                              callback_data=str(CHAT_CHILD))],
        [InlineKeyboardButton(text="Ретинопатия", callback_data=str(RETINOPATIA))],
        [InlineKeyboardButton(text="Шунтята", callback_data=str(SHUNTATA))],
        [InlineKeyboardButton(text="Бабушки торопыжек", callback_data=str(GRANDMOTHERS))],
        [InlineKeyboardButton(text="Отвести душу и поплакать", callback_data=str(CRY))],
        [InlineKeyboardButton(text="Мамы ангелов", callback_data=str(ANGELS))],
        [InlineKeyboardButton(text="Ретинопатия недоношенных 4-5 стадии", callback_data=str(RETINOPATIA_4_5))],
        [InlineKeyboardButton(text="Зрение детей с офтальмологическими проблемами", callback_data=str(PROBLEMS))],
        [InlineKeyboardButton(text="Группа поддержки в Телеграмм «Помощь семьям торопыжек» t.me/toropizhki",
                              callback_data=str(TELECRAM_CHAT))],
        [InlineKeyboardButton(text="Возврат в главное меню", callback_data=str(END))]

    ]
    keyboard = InlineKeyboardMarkup(buttons_chat)
    # If we collect features for a new person, clear the cache and save the gender
    if not context.user_data.get(START_OVER):
        context.user_data[CHAT] = {CHAT: update.callback_query.data}
        text = "Выберите чат для вступления:"

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = "Мы получили от Вас информацию!"
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_CHAT



async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в главное меню"""
    context.user_data[START_OVER] = True
    await start(update, context)

    return END

async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сбор информации для вступления в чат"""
    context.user_data[CURRENT_CHAT] = update.callback_query.data
    questions = ['ФИО мамы(или папы)', 'Ваш телефонные номер', 'ФИО ребенка', 'Дата рождения', 'Место рождения'
                 'Срок рождения', 'Вес', 'Рост', 'Диагнозы', 'Проведенные операции', 'Дата операции',
                 'Место операции', 'Дата обращения', 'Как узнали про фонд?']
    for question in questions:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=question)

    return TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Сохранение информации полученной для вступления в чат"""
    user_data = context.user_data
    user_data[CHAT][user_data[CURRENT_CHAT]] = update.message.text

    user_data[START_OVER] = True

    return await select_chat(update, context)

async def end_describing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End gathering of features and return to parent conversation."""


    # Print upper level menu
    if level == SELF:
        user_data[START_OVER] = True
        await start(update, context)
    else:
        await select_level(update, context)

    return END



async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Выход из бота из подменю"""
    await update.message.reply_text('Будем рады видеть Вас на нашем сайте! \n '
                                    'https://fond-providenie.ru')

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
description_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                select_chat, pattern="^" + str(CHAT) + "$"
            )
        ],
        states={
            SELECTING_CHAT: [
                CallbackQueryHandler(ask_for_input, pattern="^(?!" + str(END) + ").*$")
            ],
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
        },
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # Return to second level menu
            END: SELECTING_LEVEL,
            # End conversation altogether
            STOPPING: STOPPING,
        },
    )

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

