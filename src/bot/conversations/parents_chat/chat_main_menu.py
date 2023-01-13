from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import states


(
    CHAT_BABY,
    CHAT_CHILD,
    CHAT_RETINOPATIA,
    CHAT_SHUNTATA,
    CHAT_GRANDMOTHERS,
    CHAT_CRY,
    CHAT_ANGELS,
    CHAT_RETINOPATIA_4_5,
    CHAT_PROBLEMS,
    CHAT_REHABILITATION,
    CHAT_TELECRAM,
) = map(chr, range(100, 112))

(CURRENT_CHAT, SELECTING_CHAT) = map(chr, range(120, 122))


END = ConversationHandler.END


async def select_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Выбрать чат"""
    chat = update.callback_query.data
    context.user_data[CURRENT_CHAT] = chat
    buttons_chat = [
        [
            InlineKeyboardButton(
                text="Дети, рожде‌нные раньше срока (до 1,5)",
                callback_data=str(states.CHAT_BABY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Дети, рожде‌нные раньше срока (от 1,5)",
                callback_data=str(states.CHAT_CHILD),
            )
        ],
        [
            InlineKeyboardButton(
                text="Ретинопатия", callback_data=str(states.CHAT_RETINOPATIA)
            )
        ],
        [
            InlineKeyboardButton(
                text="Шунтята", callback_data=str(states.CHAT_SHUNTATA)
            )
        ],
        [
            InlineKeyboardButton(
                text="Бабушки торопыжек",
                callback_data=str(states.CHAT_GRANDMOTHERS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Отвести душу и поплакать",
                callback_data=str(states.CHAT_CRY),
            )
        ],
        [
            InlineKeyboardButton(
                text="Мамы ангелов", callback_data=str(states.CHAT_ANGELS)
            )
        ],
        [
            InlineKeyboardButton(
                text="Ретинопатия недоношенных 4-5 стадии",
                callback_data=str(states.CHAT_RETINOPATIA_4_5),
            )
        ],
        [
            InlineKeyboardButton(
                text="Дети с офтальмологическими проблемами",
                callback_data=str(states.CHAT_PROBLEMS),
            )
        ],
        [
            InlineKeyboardButton(
                text="Чат 'Реабилитация зрения'",
                callback_data=str(states.CHAT_REHABILITATION),
            )
        ],
        [
            InlineKeyboardButton(
                text="«Семьи торопыжек» t.me/toropizhki",
                callback_data=str(states.CHAT_TELEGRAM),
            )
        ],
        [
            InlineKeyboardButton(
                text="Возврат в главное меню", callback_data=str(END)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons_chat)
    text = "Выберите чат для вступления:"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text, reply_markup=keyboard
    )

    return SELECTING_CHAT
