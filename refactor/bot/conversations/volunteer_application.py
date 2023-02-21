from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import states, callbacks, const
from core.logger import logger  # noqa


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["modifying"] = False

    context.user_data[const.CURRENT_FEATURE] = 0
    context.user_data[const.FEATURES] = {}

    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Начать заполнение анкеты',
            callback_data=callbacks.START_DATA_COLLECTION
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK,
        )],
    ])

    await query.edit_message_text(
        text=f'Спасибо за интерес! Вам нужно будет предоставить информацию для куратора.',
        reply_markup=markup)

    return states.VOLONTER_CONFIRMATION

async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data["modifying"] == False:
        current_question_num = context.user_data[const.CURRENT_FEATURE]
        current_question = const.VOLONTEER_QUESTIONS[current_question_num]
    else:
        current_question = update.callback_query.data
        context.user_data[const.CURRENT_FEATURE] = const.VOLONTEER_QUESTIONS.index(current_question)

    text = const.short_questionnaire[current_question]["question"]

    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text(text=text)
    else:
        await update.message.reply_text(text=text)

    return states.VOLONTER_TYPING

async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[const.FEATURES][user_data[const.CURRENT_FEATURE]] = update.message.text

    if (
        context.user_data["modifying"]
        or (user_data[const.CURRENT_FEATURE] + 1) >= len(const.VOLONTEER_QUESTIONS)
    ):
        return await show_data(update, context)

    user_data[const.CURRENT_FEATURE] = user_data[const.CURRENT_FEATURE] + 1
    return await ask_for_input(update, context)

async def change_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data["modifying"] = True

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            const.short_questionnaire["VOLONTER_INFO_FIO"]['value'],
            callback_data=callbacks.VOLONTER_INFO_FIO
        )],
        [InlineKeyboardButton(
            const.short_questionnaire["VOLONTER_INFO_BIRTHDAY"]['value'],
            callback_data=callbacks.VOLONTER_INFO_BIRTHDAY
        )],
        [InlineKeyboardButton(
            const.short_questionnaire["VOLONTER_INFO_CITY"]['value'],
            callback_data=callbacks.VOLONTER_INFO_CITY
        )],
        [InlineKeyboardButton(
            const.short_questionnaire["VOLONTER_INFO_PHONE"]['value'],
            callback_data=callbacks.VOLONTER_INFO_PHONE
        )],
        [InlineKeyboardButton(
            const.short_questionnaire["VOLONTER_INFO_EMAIL"]['value'],
            callback_data=callbacks.VOLONTER_INFO_EMAIL
        )],
        [InlineKeyboardButton(
            const.short_questionnaire["VOLONTER_INFO_HELP"]['value'],
            callback_data=callbacks.VOLONTER_INFO_HELP
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

    return states.VOLONTER_CHOOSING

async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    text = ""
    for i in range(0, len(const.VOLONTEER_QUESTIONS)):
        text += f"{const.short_questionnaire[const.VOLONTEER_QUESTIONS[i]]['value']}:"\
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

    return states.VOLONTER_CONFIRMATION
