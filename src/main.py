from telegram.ext import Application

import core.logger  # noqa
from core.settings import TELEGRAM_TOKEN


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.run_polling()


if __name__ == "__main__":
    main()
