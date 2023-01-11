from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


TEXT_START_BUTTON = """
    Привет! Я бот-помощник Фонда помощи недоношенным детям
    и их семьям «Провидение».
    Мы  спасаем зрение недоношенным детям!
    Я помогу вам узнать как получить и оказать помощь.
"""
(
    WEBSITE,
    VK,
    INSTAGRAM,
    FACEBOOK,
    TG_CHANEL,
    TG_BOT,
) = map(chr, range(10, 16))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод приветствия."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=TEXT_START_BUTTON
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция, отображающая меню со ссылками на страницы фонда."""
    text = "Выберите интересующую вас соцсеть/страницу"
    buttons = [
        [
            InlineKeyboardButton(
                text="Интернет сайт", callback_data=str(WEBSITE)
            )
        ],
        [InlineKeyboardButton(text="VK", callback_data=str(VK))],
        [InlineKeyboardButton(text="Instagram", callback_data=str(INSTAGRAM))],
        [InlineKeyboardButton(text="Facebook", callback_data=str(FACEBOOK))],
        [
            InlineKeyboardButton(
                text="Новостной канал в ТГ", callback_data=str(TG_CHANEL)
            )
        ],
        [
            InlineKeyboardButton(
                text="Приглашение в чат бот", callback_data=str(TG_BOT)
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(text=text, reply_markup=keyboard)
