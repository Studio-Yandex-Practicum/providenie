import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from telegram import Bot
from telegram.ext import ApplicationBuilder

from app.models.models import Group, Message

from bot.ratelimiter import (
    RateLimiter,
    ptb_post_init,
    send_message,
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
rate_limiter = RateLimiter(rate_limit=30)
application = ApplicationBuilder().token(
    TELEGRAM_TOKEN).post_init(ptb_post_init).build()
job_queue = application.job_queue


@app.get('/', response_class=HTMLResponse)
async def read_form(request: Request) -> HTMLResponse:
    """Отображает HTML-форму для ввода данных."""
    return templates.TemplateResponse('form.html', {'request': request})


@app.post('/send_message/')
async def send_message_endpoint(
    request: Request,
    message: str = Form(...),
    group_id: int = Form(...),
    send_time: str = Form(...),
    photo: UploadFile = File(None),
    )-> HTMLResponse:
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

            new_message = Message(text=message,
                                  send_on=send_time_dt, is_send=False)
            new_message.groups.append(group)
            session.add(new_message)
            await session.commit()

            send_time = (send_time_dt
                         if send_time_dt >= datetime.now()
                         else datetime.now() + timedelta(seconds=10))

            job_queue.run_once(
                send_message,
                when=send_time.timestamp(),
                context={'message_id': new_message.id},
                name=f'send_mes_{new_message.id}',
            )

    return templates.TemplateResponse('success.html',
                                      {'request': request,
                                       'message': 'Сообщение запланировано!'},
                                       )
