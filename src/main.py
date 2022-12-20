import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application


load_dotenv()
token = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(token).build()

    application.run_polling()


if __name__ == "__main__":
    main()
