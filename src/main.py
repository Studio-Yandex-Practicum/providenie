import multiprocessing

import uvicorn
from telegram import Update

from app.main import app  # Импорт FastAPI-приложения

from bot.services import init_bot


def run_bot() -> None:
    """Запуск Telegram бота."""
    application = init_bot()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def run_fastapi() -> None:
    """Запуск FastAPI."""
    uvicorn.run(app, host='0.0.0.0', port=8000)


def run_both() -> None:
    """Запуск Telegram бота и FastAPI в разных процессах."""
    bot_process = multiprocessing.Process(target=run_bot)
    fastapi_process = multiprocessing.Process(target=run_fastapi)

    # Запускаем процессы
    bot_process.start()
    fastapi_process.start()

    # Ждем завершения процессов
    bot_process.join()
    fastapi_process.join()


if __name__ == '__main__':
    run_both()
