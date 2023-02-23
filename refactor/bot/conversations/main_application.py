from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import callbacks, states
from bot.constants.buttons import forms_buttons
from bot.constants.info.share import SHARE_LINKS
from core.logger import logger  # noqa


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup([
        *forms_buttons,
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
        [InlineKeyboardButton(  # TODO Перенеси в константы
            'Сделать пожертвование', url="https://fond-providenie.ru/help-chidren/sdelat-pozhertovanie/sdelat-pozhertvovanie-s-bankovskoj-karty/"
        )],
        [
            InlineKeyboardButton(
                'Задать вопрос', callback_data=callbacks.MENU_ASK_Q
            ),
            InlineKeyboardButton(
                'Узнать о фонде', callback_data=callbacks.MENU_ABOUT
            )
        ],
    ])

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(text='Я хочу...', reply_markup=markup)
    else:
        await update.message.reply_text(text='Я хочу...', reply_markup=markup)

    return states.MAIN_MENU


async def tell_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            SHARE_LINKS["TELL_WEBPAGE"]['name'],
            callback_data=callbacks.TELL_WEBPAGE
        )],
        [InlineKeyboardButton(
            SHARE_LINKS["TELL_VK"]['name'],
            callback_data=callbacks.TELL_VK
        )],
        [InlineKeyboardButton(
            SHARE_LINKS["TELL_INSTA"]['name'],
            callback_data=callbacks.TELL_INSTA
        )],
        [InlineKeyboardButton(
            SHARE_LINKS["TELL_FACEBOOK"]['name'],
            callback_data=callbacks.TELL_FACEBOOK
        )],
        [InlineKeyboardButton(
            SHARE_LINKS["TELL_CHAT"]['name'],
            callback_data=callbacks.TELL_CHAT
        )],
        [InlineKeyboardButton(
            SHARE_LINKS["TELL_TELEGRAM"]['name'],
            callback_data=callbacks.TELL_TELEGRAM
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.BACK
        )],
    ])

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Выбрать чем поделиться:', reply_markup=markup)

    return states.MAIN_MENU


async def give_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link_selection = update.callback_query.data
    link = SHARE_LINKS[link_selection]['link']
    link_info = SHARE_LINKS[link_selection]['desc']

    query = update.callback_query
    await query.answer()

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f'Перейти {link_info}',
            url=link
        )],
        [InlineKeyboardButton(
            'Назад', callback_data=callbacks.MENU_TELL_FRIEND,
        )],
    ])

    await query.edit_message_text(
        text=f'Ссылка: {link}',
        reply_markup=markup)

    return states.MAIN_MENU


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

    return states.MAIN_MENU


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    await update.message.reply_text("Until next time!")

    return ConversationHandler.END