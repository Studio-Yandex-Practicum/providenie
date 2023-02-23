from bot.sevices import init_bot
from core.logger import logger  # noqa


def main() -> None:
    application = init_bot()
    application.run_polling()


if __name__ == "__main__":
    main()
