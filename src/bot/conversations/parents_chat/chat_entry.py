from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import states


(CURRENT_CHAT, SELECTING_CHAT, ENTRY_CHAT, ENTERING_CHAT) = map(
    chr, range(120, 124)
)


(
    CHAT_PARENTS_NAME,
    CHAT_PARENTS_PHONE,
    CHAT_CHILD_NAME,
    CHAT_CHILD_BIRTHDAY,
    CHAT_CHILD_PLACE_BIRTHDAY,
    CHAT_CHILD_TERM,
    CHAT_CHILD_WEIGHT,
    CHAT_CHILD_HEIGHT,
    CHAT_CHILD_DIAGNOSE,
    CHAT_CHILD_OPERATION,
    CHAT_DATE_ADDRESS,
    CHAT_ABOUT_FOND,
) = map(chr, range(140, 153))


END = ConversationHandler.END
(START_OVER, STOPPING) = map(chr, range(160, 102))


async def enter_chat_baby(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "В группе информационная и психологическая помощь "
        "родителям по любым вопросам, "
        "связанным с недоношенными детьми младше 1,5 лет."
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "В группе информационная и психологическая помощь "
        "родителям по любым вопросам, "
        "связанным с недоношенными детьми старше 1,5 лет."
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_retinopatia(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Группа для родителей деток с ретинопатией"
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_shuntata(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Группа для родителей деток с шунтами"
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_grandmothers(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Бабушки хотят помочь своим детям, внукам, "
        "но не знают как. "
        "При этом, сами нуждаются в поддержке! "
        "Именно поэтому, создана группа "
        "взаимной поддержки бабушек недоношенных детей."
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(states.SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_cry(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Иногда очень хочется пожаловаться и поплакать. "
        "Ведь вокруг так много несправедливости! "
        "ЧАТ психологической направленности. "
        "В чате всегда готовы помочь Вам "
        "профессиональные психологи и, конечно, мамы."
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_angels(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Чат для родителей, которые столкнулись со смертью ребенка."
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_retinopatia_4_5(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Чат для родителей детей с ретинопатией недоношенных 4-5 стадии"
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_problems(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()

    text = (
        "Чат для родителей детей с различными "
        "офтальмологическими проблемами (включая косоглазие)"
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_rehabilitation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Чат реабилитация зрения"""
    await update.callback_query.answer()

    text = (
        "Чат для родителей детей, нуждающихся в реабилитации зрения"
        "Для вступления в чат Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT


async def enter_chat_telegram(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Группа в Телеграмм"""
    await update.callback_query.answer()

    text = (
        "Группа поддержки в Телеграмм "
        "«Помощь семьям торопыжек» t.me/toropizhki"
        "Для вступления в группу Вам необходимо предоставить информацию для куратора."
    )

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(SELECTING_CHAT),
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data=str(states.END)
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return states.ENTERING_CHAT
