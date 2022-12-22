from telegram.ext import CommandHandler

import core.logger  # noqa
from bot.conversations.menu import start
from bot.services import start_bot


def main() -> None:
    application = start_bot()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    

if __name__ == "__main__":
    main()
