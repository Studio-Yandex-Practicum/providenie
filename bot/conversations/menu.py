from telegram import Update
from telegram.ext import ContextTypes


TEXT_START_BUTTON ="""
    Привет! Я бот-помощник Фонда помощи недоношенным детям и их семьям «Провидение».
    Мы  спасаем зрение недоношенным детям!
    Я помогу вам узнать как получить и оказать помощь.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод приветствия."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TEXT_START_BUTTON)
