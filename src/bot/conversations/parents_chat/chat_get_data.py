from telegram import Update
from telegram.ext import ContextTypes

from .chat_show_data import chat_show_data
from bot import states


async def entering_chat(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем ФИО родителя."""
    user_data = context.user_data
    user_data[states.CHAT_FEATURES] = {states.LEVEL: states.ENTRY_CHAT}
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_PARENTS_NAME
    text = "Фамилия, имя, отчество мамы(или папы)?"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return states.CHAT_GETTING_PARENTS_NAME


async def chat_getting_parents_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем ФИО, получаем номер телефона родителя"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_PARENTS_PHONE
    text = "Номер телефона мамы (или папы)?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_PARENTS_PHONE


async def chat_getting_parents_phone(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем номер телефона, получаем фамилию ребенка
    Если выбран чат "Мамы ангелов",
     переходим в режим отображения полученной информации"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message

    if user_data[states.CURRENT_CHAT] == "Мамы ангелов":
        return await chat_show_data(update, context)

    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_NAME
    text = "Фамилия, имя, отчество ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_NAME


async def chat_getting_child_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем фамилию ребенка,
    получаем дату рождения"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_BIRTHDAY
    text = "Дата рождения ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_BIRTHDAY


async def chat_getting_child_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату рождения ребенка,
    получаем место рождения ребенка"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_PLACE_BIRTHDAY
    text = "Место рождения ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_PLACE_BIRTHDAY


async def chat_getting_child_place_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем место рождения ребенка,
    получаем срок беременности при рождении ребенка"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_TERM
    text = "Срок беременности при рождении ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_TERM


async def chat_getting_child_term(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем срок беременности рождения ребенка,
    получаем вес ребенка при рождении"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_WEIGHT
    text = "Вес ребенка при рождении?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_WEIGHT


async def chat_getting_child_weight(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем вес ребенка, получаем рост ребенка при рождении"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_HEIGHT
    text = "Рост ребенка при рождении?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_HEIGHT


async def chat_getting_child_height(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем рост ребенка, получаем данные о диагнозах"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_DIAGNOSE
    text = "Диагнозы у ребенка?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_DIAGNOSE


async def chat_getting_child_diagnose(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем диагнозы ребенка, получаем данные об операциях"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_CHILD_OPERATION
    text = "Были ли проведены операции? Дата и место операций?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_CHILD_OPERATION


async def chat_getting_child_operation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем данные об операциях,
    получаем информацию о том, как узнали о фонде"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    user_data[states.CHAT_CURRENT_FEATURE] = states.CHAT_ABOUT_FOND
    text = "Как Вы узнали о фонде?"
    await update.message.reply_text(text=text)
    return states.CHAT_GETTING_ABOUT_FOND


async def chat_getting_about_fond(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем информацию о том, как узнали о фонде,
    переходим в режим отображения полученной информации"""
    user_data = context.user_data
    message = update.message.text
    user_data[states.CHAT_FEATURES][
        user_data[states.CHAT_CURRENT_FEATURE]
    ] = message
    return await chat_show_data(update, context)
