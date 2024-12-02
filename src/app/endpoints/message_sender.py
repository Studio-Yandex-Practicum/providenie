import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from telegram import Bot
from telegram.ext import ApplicationBuilder

from app.models.models import Base, Group, Message

from bot.ratelimiter import (
    RateLimiter,
    load_unsent_messages,
    send_delayed_message,
)

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

app = FastAPI()
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), '../templates'),
)
static_dir = os.path.normpath(os.path.abspath
                              (os.path.join(os.path.dirname(__file__),
                                            '../../static')))
app.mount('/static', StaticFiles(directory=static_dir), name='static')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
job_queue = application.job_queue
rate_limiter = RateLimiter(rate_limit=30)


@app.get('/', response_class=HTMLResponse)
async def read_form(request: Request) -> HTMLResponse:
    """Отображает HTML-форму для ввода данных."""
    return templates.TemplateResponse('form.html', {'request': request})


@app.post('/send_message/')
async def send_message(
    request: Request,
    message: str = Form(...),
    group_id: int = Form(...),
    send_time: str = Form(...),
    photo: UploadFile = File(None),
    background_tasks: BackgroundTasks = None)-> HTMLResponse:
    """Обрабатывает запрос на отправку сообщения в определенной группе."""
    try:
        send_time_dt = datetime.fromisoformat(send_time)
    except ValueError:
        return templates.TemplateResponse('error.html',
                                          {'request': request,
                                           'message': 'Неверный формат даты'})

    async with SessionLocal() as session:
        async with session.begin():
            group = await session.get(Group, group_id)
            if not group:
                return templates.TemplateResponse('error.html',
                                                   {'request': request,
                                                    'message':
                                                     'Группа не найдена'})

            user_ids = [user.tg_id for user in group.users]
            new_message = Message(text=message,
                                  send_on=send_time_dt, is_send=False)
            session.add(new_message)
            await session.commit()

    for user_id in user_ids:

        await rate_limiter.send_message(send_delayed_message,
                                        context=(user_id, message, photo))

    return templates.TemplateResponse('success.html',
                                      {'request': request,
                                       'message': 'Сообщение запланировано!'},
                                       )


@app.on_event('startup')
async def startup_event()->None:
    """Событие старта приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await load_unsent_messages()
