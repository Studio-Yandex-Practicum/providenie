from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states


chat_description = {
    states.CHAT_BABY: {
        "name": "Чат для родителей детей, рожде‌нных раньше срока (до 1,5 лет)",
        "description": (
            "В группе для родителей детей, рожде‌нных раньше срока,"
            "информационная и психологическая помощь "
            "родителям по любым вопросам, "
            "связанным с недоношенными детьми младше 1,5 лет. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_CHILD: {
        "name": "Чат для родителей детей, рожде‌нных раньше срока (старше 1,5 лет)",
        "description": (
            "В группе для родителей детей, рожде‌нных раньше срока,"
            "информационная и психологическая помощь "
            "родителям по любым вопросам, "
            "связанным с недоношенными детьми старше 1,5 лет. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_RETINOPATIA: {
        "name": "Чат для родителей детей с ретинопатией",
        "description": (
            "Группа для родителей деток с ретинопатией. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_SHUNTATA: {
        "name": "Шунтята",
        "description": (
            "Группа для родителей деток с шунтами. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_GRANDMOTHERS: {
        "name": "Бабушки торопыжек",
        "description": (
            "Группа для бабушек "
            "Бабушки хотят помочь своим детям, внукам, "
            "но не знают как. "
            "При этом, сами нуждаются в поддержке! "
            "Именно поэтому, создана группа "
            "взаимной поддержки бабушек недоношенных детей. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_CRY: {
        "name": "Отвести душу и поплакать",
        "description": (
            "Иногда очень хочется пожаловаться и поплакать. "
            "Ведь вокруг так много несправедливости! "
            "Чат психологической направленности. "
            "В чате всегда готовы помочь Вам "
            "профессиональные психологи и, конечно, мамы. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_ANGELS: {
        "name": "Мамы ангелов",
        "description": (
            "Чат для родителей, которые столкнулись со смертью ребенка. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_RETINOPATIA_4_5: {
        "name": "Ретинопатия недоношенных 4-5 стадии",
        "description": (
            "Чат для родителей детей с ретинопатией недоношенных 4-5 стадии. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_PROBLEMS: {
        "name": "Дети с офтальмологическими проблемами",
        "description": (
            "Чат для родителей детей с различными "
            "офтальмологическими проблемами (включая косоглазие). "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_REHABILITATION: {
        "name": "Реабилитация зрения",
        "description": (
            "Чат для родителей детей, нуждающихся в реабилитации зрения. "
            "Для вступления в чат Вам необходимо предоставить информацию для куратора."
        ),
    },
    states.CHAT_TELEGRAM: {
        "name": "Семьи торопыжек",
        "description": (
            "Группа поддержки в Телеграмм "
            "«Помощь семьям торопыжек» t.me/toropizhki. "
            "Для вступления в группу Вам необходимо предоставить информацию для куратора."
        ),
    },
}


async def enter_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    await update.callback_query.answer()
    chat = update.callback_query.data
    user_data = context.user_data
    user_data[states.CURRENT_CHAT] = chat
    text = f'{chat_description[chat]["description"]}'
    user_data[states.CHAT_FEATURES] = {states.LEVEL: states.ENTRY_CHAT}
    user_data[states.CHAT_FEATURES][
        user_data[states.CURRENT_CHAT]
    ] = chat_description[chat]["name"]

    buttons = [
        [
            InlineKeyboardButton(
                text="Вступить в чат", callback_data=str(states.ENTRY_CHAT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Вернуться в список чатов",
                callback_data=str(states.CHAT_END),
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
