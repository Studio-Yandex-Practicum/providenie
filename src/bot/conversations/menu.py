from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler


(
    SELECTING_ACTION,
    CHATS,
    REQUEST,
    VOLUNTEER,
    TALK,
    DONATION,
    EVENTS,
    QUESTION,
    ABOUT,
) = map(chr, range(9))

END = ConversationHandler.END
(START_OVER, CURRENT_CHAT) = map(chr, range(40, 42))

(
    SELECTING_MEDIA,
    WEBSITE,
    VK,
    INSTAGRAM,
    FACEBOOK,
    TG_CHANNEL,
    TG_BOT,
) = map(chr, range(9, 16))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод приветствия."""
    text_start_button = (
        "Привет! Я бот-помощник фонда помощи "
        'недоношенным детям и их семьям "Провидение".\n '
        "Мы спасаем зрение недоношенным детям.\n"
        "Я помогу Вам как получить, так и оказать помощь!\n"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_start_button
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Главное меню бота. Выбор пункта меню"""
    text = "У фонда 'Провидение' есть следующие программы:"
    buttons = [
        [
            InlineKeyboardButton(
                text="Хочу попасть в родительский чат",
                callback_data=str(CHATS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Заявка в фонд", callback_data=str(REQUEST)
            )
        ],
        [
            InlineKeyboardButton(
                text="Хочу стать волонтером", callback_data=str(VOLUNTEER)
            )
        ],
        [
            InlineKeyboardButton(
                text="Рассказать о Фонде своим друзьям",
                callback_data=str(TALK),
            )
        ],
        [
            InlineKeyboardButton(
                text="Пожертвование", callback_data=str(DONATION)
            )
        ],
        [
            InlineKeyboardButton(
                text="Наши события", callback_data=str(EVENTS)
            ),
            InlineKeyboardButton(
                text="Задать вопрос", callback_data=str(QUESTION)
            ),
        ],
        [
            InlineKeyboardButton(text="О Фонде", callback_data=str(ABOUT)),
            InlineKeyboardButton(text="Выход", callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(reply_markup=keyboard)
    else:
        await update.message.reply_text(
            'Я бот-помощник фонда помощи "Провидение".\n '
        )
        await update.message.reply_text(reply_markup=keyboard, text=text)

    context.user_data[START_OVER] = False

    return SELECTING_ACTION


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение разговора по команде /stop"""
    await update.message.reply_html(
        text="Будем рады видеть Вас на нашем сайте! \n"
        " <b><a>https://fond-providenie.ru</a></b> "
    )
    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершение по команде из меню"""
    await update.callback_query.answer()
    text = (
        "Будем рады видеть Вас на нашем сайте! \n https://fond-providenie.ru"
    )
    await update.callback_query.edit_message_text(text=text)

    return END


async def talk_friends(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "talk_friends"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_ACTION


async def give_donation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "give_donation"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_ACTION


async def get_events(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "get_events"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_ACTION


async def ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "ask_question"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_ACTION


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.callback_query.answer()
    text = "request"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_ACTION


async def select_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    text = "select_chat"
    await update.callback_query.edit_message_text(text=text)
    return SELECTING_ACTION


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Функция, отображающая меню со ссылками на страницы фонда."""
    text = "Выберите интересующую вас соцсеть/страницу"
    buttons = [
        [
            InlineKeyboardButton(
                text="Интернет сайт", callback_data=str(WEBSITE)
            )
        ],
        [InlineKeyboardButton(text="VK", callback_data=str(VK))],
        [InlineKeyboardButton(text="Instagram", callback_data=str(INSTAGRAM))],
        [InlineKeyboardButton(text="Facebook", callback_data=str(FACEBOOK))],
        [
            InlineKeyboardButton(
                text="Новостной канал в ТГ", callback_data=str(TG_CHANNEL)
            )
        ],
        [
            InlineKeyboardButton(
                text="Приглашение в чат бот", callback_data=str(TG_BOT)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )
    return SELECTING_MEDIA


async def social_link(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Функция, отображающая ссылку выбранной соцсети."""
    social_link_dict = {
        WEBSITE: "https://fond-providenie.ru/",
        VK: "https://vk.com/fond_providenie",
        INSTAGRAM: "https://vk.com/fond_providenie",
        FACEBOOK: "https://www.facebook.com/fond.providenie/",
        TG_CHANNEL: "https://t.me/providenie_fond",
        TG_BOT: "TODO",
    }

    buttons = [
        [
            InlineKeyboardButton(
                text="В главное меню", callback_data=str(START_OVER)
            )
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(END))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query
    text = social_link_dict[query.data]

    await query.answer()
    await query.edit_message_text(text=text, reply_markup=keyboard)
    return SELECTING_MEDIA
