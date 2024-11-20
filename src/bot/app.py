import asyncio
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)

app = FastAPI()
templates = Jinja2Templates(directory='templates')

# Список пользователей. Требуется реализация подтягиваания из БД
user_ids = ['936228668']
# Очередь для сообщений
message_queue = asyncio.Queue()


async def send_message_task(
    user_id: str,
    message: str,
    file_data: Optional[dict],
) -> None:
    """Отправка текстового сообщения и/или сообщения с файлом."""
    try:
        # Отправка текстового сообщения
        await bot.send_message(chat_id=user_id, text=message)

        # Если файл загружен, отправляем его
        if file_data:
            await bot.send_document(
                chat_id=user_id,
                document=file_data['file'],
                filename=file_data['filename'],
            )

        print(f'Сообщение успешно отправлено пользователю {user_id}')
    except TelegramError as e:
        print(f'Ошибка при отправке сообщения пользователю {user_id}: {e}')


async def message_worker() -> None:
    """Ограничение до 30 сообщений в секунду."""
    while True:
        user_id, message, file_data = await message_queue.get()
        await send_message_task(user_id, message, file_data)
        await asyncio.sleep(1 / 30)


@app.on_event('startup')
async def startup_event() -> None:
    """Запуск рабочего процесса отправки сообщений."""
    asyncio.create_task(message_worker())


@app.get('/', response_class=HTMLResponse)
async def read_form(request: Request) -> HTMLResponse:
    """Обрабатываем GET-запрос и возращаем HTML-форму."""
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/', response_class=HTMLResponse)
async def send_message(
    request: Request,
    message: str = Form(...),
    file: UploadFile = File(None),
) -> HTMLResponse:
    """Обработка запроса на отправку сообщения пользователям."""
    status = ''
    file_data = None
    if file:
        # Чтение файла в память
        file_data = {
            'file': await file.read(),
            'filename': file.filename,
        }

    for user_id in user_ids:
        await message_queue.put((user_id, message, file_data))

    status = f'Сообщение отправлено: "{message}"'

    return templates.TemplateResponse(
        'index.html',
        {'request': request, 'status': status},
    )


async def scheduled_task(
    user_id: str,
    message: str,
    file_data: Optional[dict],
    delay: int,
) -> None:
    """Запланирована задача для отправки сообщения пользователям."""
    await asyncio.sleep(delay)  # Какое время указать?
    await send_message_task(user_id, message, file_data)


@app.post('/schedule', response_class=HTMLResponse)
async def schedule_message(
    request: Request,
    delay: int = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None),
) -> HTMLResponse:
    """Планирует отправку сообщения пользователям с заданной задержкой."""
    file_data = None
    if file:
        file_data = {'file': await file.read(), 'filename': file.filename}

    for user_id in user_ids:
        asyncio.create_task(scheduled_task(user_id, message, file_data, delay))

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'success': f'Сообщения запланированы через {delay} секунд!',
        },
    )
