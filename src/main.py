import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.endpoints.routers import main_router

from bot.core import logger  # noqa
from bot.services import init_bot

app = FastAPI(debug=True)

app.include_router(main_router)


# Убедитесь, что правильный путь к папке статических файлов
app.mount(
    '/static',
    StaticFiles(directory='app/endpoints/static'),
    name='static',
)


async def run_bot() -> None:
    """Launch the Telegram bot."""
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
    asyncio.run(main())
