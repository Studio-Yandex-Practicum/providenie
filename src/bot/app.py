import asyncio
import os
from typing import AsyncGenerator, List, Optional

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Bot
from telegram.error import TelegramError

from src.app.core.db import get_async_session
from src.app.crud.user_tg import crud_user
from src.app.models.models import Message, Photo

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)


app = FastAPI()

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), '../templates')
)
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.mount('/static', StaticFiles(directory=static_dir), name='static')
message_queue = asyncio.Queue()


async def send_message(
    tg_id: str, message: str, file_data: Optional[dict]
) -> None:
    """Отправляет сообщение или фото в Telegram."""
    try:
        if file_data:
            await bot.send_photo(
                chat_id=tg_id, photo=file_data['file'], caption=message
            )
        else:
            await bot.send_message(chat_id=tg_id, text=message)
    except TelegramError as e:
        print(f'Ошибка при отправке сообщения: {e}')


async def process_queue() -> None:
    """Обрабатывает очередь сообщений, отправляя их пользователям."""
    while True:
        tg_id, message, file_data = await message_queue.get()
        await send_message(tg_id, message, file_data)
        await asyncio.sleep(1 / 30)
        # Ожидание 1/30 секунды перед отправкой


async def send_messages(
    file: Optional[UploadFile],
    message: str,
    user_ids: List[int],
    request: Request,
    session: AsyncSession,
) -> HTMLResponse:
    """Отправляет сообщения пользователям и сохраняет их в базе данных."""
    file_data = None

    if file and file.content_type.startswith('image/'):
        file_data = {
            'file': await file.read(),
            'filename': file.filename,
        }

    try:
        for tg_id in user_ids:
            await message_queue.put((tg_id, message, file_data))
            db_message = Message(
                text=message,
                create_user=tg_id,
                update_users=tg_id,
            )
            session.add(db_message)

        await session.commit()

        if file_data:
            for tg_id in user_ids:
                db_photo = Photo(
                    filename=file_data['filename'],
                    message_id=db_message.id,
                )
                session.add(db_photo)

            await session.commit()

        status = f'Сообщение отправлено: "{message}"'
    except Exception as e:
        status = f'Ошибка при отправке сообщения: {str(e)}'

    return templates.TemplateResponse(
        'create_messages.html', {'request': request, 'status': status}
    )


async def post_init() -> None:
    """Выполняет операции инициализации после запуска бота."""
    print('Бот успешно инициализирован.')


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Управляет жизненным циклом приложения FastAPI."""
    task = asyncio.create_task(process_queue())
    await post_init()
    yield
    task.cancel()


@app.get('/', response_class=HTMLResponse)
async def read_form(request: Request) -> HTMLResponse:
    """Отображает форму для отправки сообщений."""
    return templates.TemplateResponse(
        'create_messages.html', {'request': request}
    )


@app.post('/', response_class=HTMLResponse)
async def handle_send_message(
    request: Request,
    message: str = Form(...),
    file: UploadFile = File(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Обрабатывает POST-запрос, отправляя сообщения пользователям."""
    try:
        users = await crud_user.get_all_users(session)
        user_ids = [user.tg_id for user in users]
        return await send_messages(file, message, user_ids, request, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def scheduled_task(
    tg_id: str,
    message: str,
    file_data: Optional[dict],
    delay: int,
) -> None:
    """Запланированная задача для отправки сообщения после задержки."""
    await asyncio.sleep(delay)
    await send_messages(file_data, message, [tg_id], Request)
    # Возврат в основной поток


@app.post('/schedule', response_class=HTMLResponse)
async def schedule_message(
    request: Request,
    delay: int = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Запускает процесс отправки сообщений с заданной задержкой."""
    user_ids = [userid.id for userid in await crud_user.get_all_users(session)]
    if file:
        file_data = {'file': await file.read(), 'filename': file.filename}
    else:
        file_data = None
    for tg_id in user_ids:
        asyncio.create_task(scheduled_task(tg_id, message, file_data, delay))

    return templates.TemplateResponse(
        'create_messages.html',
        {
            'request': request,
            'success': f'Сообщения запланированы через {delay} секунд!',
        },
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
