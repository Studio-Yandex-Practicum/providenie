from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from .chat_show_data import chat_show_data
from bot import constants as const
from bot import keys as key
from bot import states as state


async def ask_full_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Начинаем поочерёдный ввод данных. Спрашиваем ФИО родителя."""
    user_data = context.user_data
    user_data[key.CHAT_FEATURES] = {key.LEVEL: key.ENTRY_CHAT}
    user_data[key.CHAT_CURRENT_FEATURE] = key.CHAT_PARENTS_NAME
    if user_data[key.CURRENT_CHAT] == "Бабушки торопыжек":
        text = const.MSG_CHAT_GRANDMOTHERS_NAME
    else:
        text = const.MSG_CHAT_PARENTS_NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return state.CHAT_GETTING_PARENTS_NAME


async def save_chat_feature(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    next_feature: Optional[str] = None,
    reply_text: Optional[str] = None,
):
    """Сохраняем данные аттрибута"""
    user_data = context.user_data
    message = update.message.text
    user_data[key.CHAT_FEATURES][user_data[key.CHAT_CURRENT_FEATURE]] = message
    if next_feature:
        user_data[key.CHAT_CURRENT_FEATURE] = next_feature
    if reply_text:
        await update.message.reply_text(text=reply_text)


async def ask_phone_number(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем ФИО, получаем номер телефона родителя"""
    if context.user_data[key.CURRENT_CHAT] == "Бабушки торопыжек":
        text = const.MSG_CHAT_GRANDMOTHERS_PHONE
    else:
        text = const.MSG_CHAT_PARENTS_PHONE

    await save_chat_feature(
        update, context, next_feature=key.CHAT_PARENTS_PHONE, reply_text=text
    )
    return state.CHAT_GETTING_PARENTS_PHONE


async def ask_full_name_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем номер телефона, получаем фамилию ребенка
    Если выбран чат "Мамы ангелов",
     переходим в режим отображения полученной информации"""
    user_data = context.user_data

    if user_data[key.CURRENT_CHAT] == "Мамы ангелов":
        await save_chat_feature(update, context)
        return await chat_show_data(update, context)

    if user_data[key.CURRENT_CHAT] == "Бабушки торопыжек":
        text = const.MSG_CHAT_GRANDMOTHERS_GRANDCHILD
    else:
        text = const.MSG_CHAT_CHILD_NAME
    await save_chat_feature(
        update, context, next_feature=key.CHAT_CHILD_NAME, reply_text=text
    )
    return state.CHAT_GETTING_CHILD_NAME


async def ask_child_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем фамилию ребенка,
    получаем дату рождения"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_BIRTHDAY,
        reply_text=const.MSG_CHAT_CHILD_BIRTHDAY,
    )
    return state.CHAT_GETTING_CHILD_BIRTHDAY


async def ask_place_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем дату рождения ребенка,
    получаем место рождения ребенка"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_PLACE_BIRTHDAY,
        reply_text=const.MSG_CHAT_CHILD_PLACE_BIRTHDAY,
    )
    return state.CHAT_GETTING_CHILD_PLACE_BIRTHDAY


async def ask_child_term(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем место рождения ребенка,
    получаем срок беременности при рождении ребенка"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_TERM,
        reply_text=const.MSG_CHAT_CHILD_TERM,
    )
    return state.CHAT_GETTING_CHILD_TERM


async def ask_child_weight(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем срок беременности рождения ребенка,
    получаем вес ребенка при рождении"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_WEIGHT,
        reply_text=const.MSG_CHAT_CHILD_WEIGHT,
    )
    return state.CHAT_GETTING_CHILD_WEIGHT


async def ask_child_height(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем вес ребенка, получаем рост ребенка при рождении"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_HEIGHT,
        reply_text=const.MSG_CHAT_CHILD_HEIGHT,
    )
    return state.CHAT_GETTING_CHILD_HEIGHT


async def ask_child_diagnose(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем рост ребенка, получаем данные о диагнозах"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_DIAGNOSE,
        reply_text=const.MSG_CHAT_CHILD_DIAGNOSE,
    )
    return state.CHAT_GETTING_CHILD_DIAGNOSE


async def ask_child_operation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем диагнозы ребенка, получаем данные об операциях"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_CHILD_OPERATION,
        reply_text=const.MSG_CHAT_CHILD_OPERATION,
    )
    return state.CHAT_GETTING_CHILD_OPERATION


async def ask_about_fond(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем данные об операциях,
    получаем информацию о том, как узнали о фонде"""
    await save_chat_feature(
        update,
        context,
        next_feature=key.CHAT_ABOUT_FOND,
        reply_text=const.MSG_CHAT_ABOUT_FOND,
    )
    return state.CHAT_GETTING_ABOUT_FOND


async def display_all_entered_value(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Сохраняем информацию о том, как узнали о фонде,
    переходим в режим отображения полученной информации"""
    await save_chat_feature(update, context)
    return await chat_show_data(update, context)
