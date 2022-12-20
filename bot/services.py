from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from core.settings import TEXT_START_BUTTON


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод приветствия."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TEXT_START_BUTTON)



application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)
