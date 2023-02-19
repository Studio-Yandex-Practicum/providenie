from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import callbacks, states
from core.logger import logger  # noqa
from .info import link_desc


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Попасть в родительский чат', callback_data=callbacks.MENU_CHAT
        )],
        [InlineKeyboardButton(
            'Отправить заявку в фонд', callback_data=callbacks.MENU_APP_FOND
        )],
        [InlineKeyboardButton(
            'Стать волонтером', callback_data=callbacks.MENU_VOLONTER
        )],
        [InlineKeyboardButton(
            'Рассказать о фонде своим друзьям', callback_data=callbacks.MENU_TELL_FRIEND
        )],
        [InlineKeyboardButton(
            'Сделать пожертвование', callback_data=callbacks.MENU_GIVE_MONEY
        )],
        [InlineKeyboardButton(
            'Задать вопрос', callback_data=callbacks.MENU_ASK_Q
        ),
        InlineKeyboardButton(
            'Узнать о фонде', callback_data=callbacks.MENU_ABOUT
        )],
    ])

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(text='Я хочу...', reply_markup=markup)
    else:
        await update.message.reply_text(text='Я хочу...', reply_markup=markup)

    return states.LEVEL_MENU


async def tell_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            link_desc["TELL_WEBPAGE"]['name'],
            callback_data=callbacks.TELL_WEBPAGE
        )],
        [InlineKeyboardButton(
            link_desc["TELL_VK"]['name'],
            callback_data=callbacks.TELL_VK
        )],
        [InlineKeyboardButton(
            link_desc["TELL_INSTA"]['name'],
            callback_data=callbacks.TELL_INSTA
        )],
        [InlineKeyboardButton(
            link_desc["TELL_FACEBOOK"]['name'],
            callback_data=callbacks.TELL_FACEBOOK
        )],
        [InlineKeyboardButton(
            link_desc["TELL_CHAT"]['name'],
            callback_data=callbacks.TELL_CHAT
        )],
        [InlineKeyboardButton(
            link_desc["TELL_TELEGRAM"]['name'],
            callback_data=callbacks.TELL_TELEGRAM
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK
        )],
    ])

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Выбрать чем поделиться:', reply_markup=markup)

    return states.LEVEL_MENU

async def give_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link_selection = update.callback_query.data
    link = link_desc[link_selection]['link']
    link_info = link_desc[link_selection]['desc']

    query = update.callback_query
    await query.answer()

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f'Перейти {link_info}',
            url=link
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK,
        )],
    ])

    await query.edit_message_text(
        text=f'Ссылка: {link}',
        reply_markup=markup)

    return states.CHAT_CONFIRMATION

async def give_donation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK
        )],
    ])
    await query.edit_message_text(text='Вот ссылка: ссылка', reply_markup=markup)

    return states.LEVEL0

async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK
        )],
    ])
    await query.edit_message_text(
        text='Информация о фонде: почитайте здесь',
        reply_markup=markup)

    return states.LEVEL0

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    await update.message.reply_text("Until next time!")

    return ConversationHandler.END
