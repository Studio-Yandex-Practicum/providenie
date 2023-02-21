from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.conversations.constants.keyboards import start_data_collection_keyboard, back_button
from bot import states
from bot.conversations.constants.forms import forms
from bot.conversations.menu import start as main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form_name = update.callback_query.data
    form = forms[form_name]
    context.user_data["FORM"] = form
    if len(form['selections']) > 1:  # Если у нас нет меню то переходим к подтверждению заполнения анкеты.
        return await show_menu(update, context)
    else:
        return await confirm_selection(update, context)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data["FORM"]
    selections = form['selections']
    if len(selections) <= 1:
        return await main_menu(update, context)
    buttons = [
        [
            InlineKeyboardButton(
                selection_data.get("name"),
                callback_data=selection_name
            )
        ] for selection_name, selection_data in selections.items()
    ]
    keyboard = InlineKeyboardMarkup([*buttons, [back_button]])

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Выбери кнопку", reply_markup=keyboard)

    return states.CHOOSING


async def confirm_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form = context.user_data["FORM"]
    selections = form['selections']
    query = update.callback_query
    selected_item_name = query.data
    selected_item = selections.get(selected_item_name)
    reply_text = selected_item.get('desc')

    context.user_data["SELECTED"] = selected_item

    await query.answer()
    await query.edit_message_text(
        text=reply_text,
        reply_markup=start_data_collection_keyboard
    )

    return states.CONFIRMATION


async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass