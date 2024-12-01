from bot.core import logger  # noqa
from bot.services import init_bot


def main() -> None:
    """Run application."""
    application = init_bot()
    await application.initialize()
    await application.start()
    await application.updater.start_polling()


async def run_fastapi() -> None:
    """Launch the FastAPI application."""
    config = uvicorn.Config(app, host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    """Run both the Telegram bot and FastAPI concurrently."""
    await asyncio.gather(run_bot(), run_fastapi())


if __name__ == '__main__':
    main()
