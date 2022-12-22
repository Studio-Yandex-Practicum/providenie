import core.logger  # noqa
from bot.services import start_bot


def main() -> None:
    application = start_bot()
    application.run_polling()


if __name__ == "__main__":
    main()
