from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import states, callbacks, const
from core.logger import logger  # noqa
from .info import chat_desc


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_BABY"]["name"],
            callback_data=callbacks.CHAT_SELECT_BABY
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_CHILD"]["name"],
            callback_data=callbacks.CHAT_SELECT_CHILD
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_RETINOPATIA"]["name"],
            callback_data=callbacks.CHAT_SELECT_RETINOPATIA
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_SHUNTATA"]["name"],
            callback_data=callbacks.CHAT_SELECT_SHUNTATA
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_GRANDMOTHERS"]["name"],
            callback_data=callbacks.CHAT_SELECT_GRANDMOTHERS
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_CRY"]["name"],
            callback_data=callbacks.CHAT_SELECT_CRY
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_ANGELS"]["name"],
            callback_data=callbacks.CHAT_SELECT_ANGELS
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_RETINOPATIA_4_5"]["name"],
            callback_data=callbacks.CHAT_SELECT_RETINOPATIA_4_5
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_RETINOPATIA"]["name"],
            callback_data=callbacks.CHAT_SELECT_RETINOPATIA
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_REHABILITATION"]["name"],
            callback_data=callbacks.CHAT_SELECT_REHABILITATION
        )],
        [InlineKeyboardButton(
            chat_desc["CHAT_SELECT_TELEGRAM"]["name"],
            callback_data=callbacks.CHAT_SELECT_TELEGRAM
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK
        )],
    ])
    await query.edit_message_text(
        text='Выберите чат в который хотите вступить',
        reply_markup=markup)

    return states.CHAT_CHOOSING


async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_selection = update.callback_query.data
    context.user_data["chat"] = chat_selection
    context.user_data["modifying"] = False

    context.user_data[const.CURRENT_FEATURE] = 0
    context.user_data[const.FEATURES] = {}

    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Подтвердить выбор чата и начать\nзаполнение анкеты',
            callback_data=callbacks.START_DATA_COLLECTION
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.MENU_CHAT,
        )],
    ])

    await query.edit_message_text(
        text=f'Вы выбрали {chat_desc[chat_selection]["name"]}.\n'
             f'{chat_desc[chat_selection]["desc"]}',
        reply_markup=markup)

    return states.CHAT_CONFIRMATION

async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data["modifying"] == False:
        current_question_num = context.user_data[const.CURRENT_FEATURE]
        current_question = const.CHAT_QUESTIONS[current_question_num]
    else:
        current_question = update.callback_query.data
        context.user_data[const.CURRENT_FEATURE] = const.CHAT_QUESTIONS.index(current_question)

    text = const.questionnaire[current_question]["question"]

    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text(text=text)
    else:
        await update.message.reply_text(text=text)

    return states.CHAT_TYPING

async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[const.FEATURES][user_data[const.CURRENT_FEATURE]] = update.message.text

    if (
        context.user_data["modifying"]
        or (user_data[const.CURRENT_FEATURE] + 1) >= len(const.CHAT_QUESTIONS)
    ):
        return await show_data(update, context)

    user_data[const.CURRENT_FEATURE] = user_data[const.CURRENT_FEATURE] + 1
    return await ask_for_input(update, context)

async def change_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data["modifying"] = True

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            const.questionnaire["INFO_FIO_MOTHER"]['value'],
            callback_data=callbacks.INFO_FIO_MOTHER
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_PHONE"]['value'],
            callback_data=callbacks.INFO_PHONE
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_FIO_CHILD"]['value'],
            callback_data=callbacks.INFO_FIO_CHILD
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_BIRTHDAY"]['value'],
            callback_data=callbacks.INFO_BIRTHDAY
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_BIRTH_DATE"]['value'],
            callback_data=callbacks.INFO_BIRTH_DATE
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_BIRTH_WEIGHT"]['value'],
            callback_data=callbacks.INFO_BIRTH_WEIGHT
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_BIRTH_HEIGHT"]['value'],
            callback_data=callbacks.INFO_BIRTH_HEIGHT
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_DIAGNOSIS"]['value'],
            callback_data=callbacks.INFO_DIAGNOSIS
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_OPERATION"]['value'],
            callback_data=callbacks.INFO_OPERATION
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_OPERATION_DATE"]['value'],
            callback_data=callbacks.INFO_OPERATION_DATE
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_OPERATION_PLACE"]['value'],
            callback_data=callbacks.INFO_OPERATION_PLACE
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_DATE"]['value'],
            callback_data=callbacks.INFO_DATE
        )],
        [InlineKeyboardButton(
            const.questionnaire["INFO_WHERE_GOT_INFO"]['value'],
            callback_data=callbacks.INFO_WHERE_GOT_INFO
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.SHOW
        )],
    ])
    text = "Выберите значение, которое хотите изменить:"
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(text=text, reply_markup=markup)
    else:
        await update.message.reply_text(text=text, reply_markup=markup)

    return states.CHAT_CHOOSING

async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    text = ""
    for i in range(0, len(const.CHAT_QUESTIONS)):
        text += f"{const.questionnaire[const.CHAT_QUESTIONS[i]]['value']}:"\
                f"{user_data[const.FEATURES].get(i, '-')}\n"

    context.user_data["modifying"] = False

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Подтвердить данные и отправить',
            callback_data=callbacks.MENU_CHAT
        )],
        [InlineKeyboardButton(
            'Изменить данные', callback_data=callbacks.INFO_CHANGE,
        )],
        [InlineKeyboardButton(
            'Отменить и вернуться в главное меню', callback_data=callbacks.BACK,
        )],
    ])

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=markup)
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=markup)

    return states.CHAT_CONFIRMATION
