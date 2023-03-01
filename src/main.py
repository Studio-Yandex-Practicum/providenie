from bot.core import logger  # noqa
from bot.services import init_bot


def main() -> None:
    application = init_bot()
    application.run_polling()


if __name__ == "__main__":
    main()
