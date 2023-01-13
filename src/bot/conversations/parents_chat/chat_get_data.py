from telegram import Update
from telegram.ext import ContextTypes

from .chat_show_data import chat_show_data
from bot import states


(
    START_OVER,
    STOPPING,
    END,
    CHAT_FEATURE,
    CURRENT_CHAT,
    SELECTING_CHAT,
    FEATURES,
    CURRENT_FEATURE,
    ENTRY_CHAT,
    ENTERING_CHAT,
    CHAT_TYPING,
    CHAT_SHOWING,
    CHAT_DATA_EDIT,
    CHAT_SEND,
) = map(chr, range(120, 134))

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


(
    CHAT_GETTING_PARENTS_SURNAME,
    CHAT_GETTING_PARENTS_PHONE,
    CHAT_GETTING_CHILD_NAME,
    CHAT_GETTING_CHILD_BIRTHDAY,
    CHAT_GETTING_CHILD_PLACE_BIRTHDAY,
    CHAT_GETTING_CHILD_TERM,
    CHAT_GETTING_CHILD_WEIGHT,
    CHAT_GETTING_CHILD_HEIGHT,
    CHAT_GETTING_CHILD_DIAGNOSE,
    CHAT_GETTING_CHILD_OPERATION,
    CHAT_GETTING_DATE_ADDRESS,
    CHAT_GETTING_ABOUT_FOND,
) = map(chr, range(160, 176))


async def entering_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем ФИО родителя."""
    user_data = context.user_data
    user_data[states.FEATURES] = {states.LEVEL: states.ENTRY_CHAT}
    user_data[states.CURRENT_FEATURE] = states.CHAT_PARENTS_NAME
    text = "Фамилия, Имя, Отчество родителя(опекуна)?"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return states.CHAT_GETTING_PARENTS_NAME


async def chat_getting_parents_surname(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем ФИО, получаем номер телефона родителя"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_PARENTS_PHONE
    text = "Ваш номер телефона?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_PARENTS_PHONE


async def chat_getting_parents_phone(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем номер телефона, получаем фамилию ребенка"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_NAME
    text = "Фамилия, имя, отчество ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_NAME


async def chat_getting_child_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем фамилию ребенка, получаем дату рождения"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_BIRTHDAY
    text = "Дата рождения ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_BIRTHDAY


async def chat_getting_child_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату рождения ребенка, получаем место рождения ребенка"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_PLACE_BIRTHDAY
    text = "Место рождения ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_PLACE_BIRTHDAY


async def chat_getting_child_place_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем место рождения ребенка, получаем срок беременности рождения ребенка"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_TERM
    text = "Срок беременности рождения ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_TERM


async def chat_getting_child_term(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем срок беременности рождения ребенка, получаем вес ребенка при рождении"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_WEIGHT
    text = "Вес ребенка при рождении?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_WEIGHT


async def chat_getting_child_weight(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем вес ребенка, получаем рост ребенка при рождении"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_HEIGHT
    text = "Рост ребенка при рождении?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_HEIGHT


async def chat_getting_child_height(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем рост ребенка, получаем данные о диагнозах"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_DIAGNOSE
    text = "Диагнозы у ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_DIAGNOSE


async def chat_getting_child_diagnose(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем диагнозы ребенка, получаем данные об операциях"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_CHILD_OPERATION
    text = "Были ли проведены операции? Дата и место операций?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_OPERATION


async def chat_getting_child_operation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем данные об операциях, получаем дату обращения в фонд"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_DATE_ADDRESS
    text = "Дата обращения"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_DATE_ADDRESS


async def chat_getting_date_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату обращения, получаем информацию о том, как узнали о фонде"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_ABOUT_FOND
    text = "Как Вы узнали о фонде?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_ABOUT_FOND


async def chat_getting_about_fond(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату обращения, получаем информацию о том, как узнали о фонде"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.FEATURES][user_data[states.CURRENT_FEATURE]] = message
    user_data[states.CURRENT_FEATURE] = states.CHAT_ABOUT_FOND
    text = "Как Вы узнали о фонде?"
    await update.message.reply_text(text=text)
    return await chat_show_data(update, context)
