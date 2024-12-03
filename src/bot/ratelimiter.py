import asyncio
import os
import logging
from collections import deque
from datetime import datetime
from typing import Any, Callable, List

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from telegram import Bot
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, ContextTypes, Application

from app.models.models import Group

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
job_queue = application.job_queue
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RateLimiter:
    """Класс для ограничения скорости отправки сообщений."""

    def __init__(self, rate_limit: int)->None:
        """Инициализация экземпляра RateLimiter."""
        self.rate_limit = rate_limit  # Max количество сообщений в секунду
        self.messages_queue = deque()  # Очередь для сообщений

    async def send_message(self, send_func: Callable[..., Any],
                           *args: Any, **kwargs: Any)->None:
        """Отправляет сообщения с соблюдением ограничения по скорости."""
        self.messages_queue.append((send_func, args, kwargs))

        if len(self.messages_queue) <= self.rate_limit:
            await self._process_queue()

    async def _process_queue(self)->None:
        while self.messages_queue:
            send_func, args, kwargs = self.messages_queue.popleft()
            await send_func(*args, **kwargs)
            await asyncio.sleep(1 / self.rate_limit)


async def load_unsent_messages()->None:
    """Загрузка неотправленных сообщений из базы данных.

    Планирование их отправки.
    """
    async with SessionLocal() as session:
        async with session.begin():
            # Получение всех неотправленных сообщений
            unsent_messages = await session.execute(
                text('SELECT * FROM message WHERE is_send = FALSE'),
                )
            for message in unsent_messages.scalars().all():
                # Преобразование строки времени в datetime
                if message.send_on > datetime.now():
                    user_ids = await get_user_ids_of_group(message.group_id,
                                                           session)
                    for user_id in user_ids:
                        job_queue.run_once(
                            send_delayed_message,
                            when=message.send_on.timestamp(),
                            context=(user_id, message.text, message.photos),
                            misfire_grace_time=None
                        )
                        message.is_send = True


async def get_user_ids_of_group(group_id: int,
                                session: AsyncSession) -> List[int]:
    """Получение идентификаторов пользователей группы."""
    group = await session.get(Group, group_id)
    return [user.tg_id for user in group.users] if group else []


rate_limiter = RateLimiter(rate_limit=30)


async def send_delayed_message(context: ContextTypes.DEFAULT_TYPE)->None:
    """Отправка задержанного сообщения."""
    user_id, message_text, photo = context.args

    async def send()-> None:
        try:
            if photo:
                await bot.send_photo(chat_id=user_id,
                                     photo=photo, caption=message_text)
            else:
                await bot.send_message(chat_id=user_id, text=message_text)
        except TelegramError as e:
            print(f'Ошибка отправки сообщения пользователю {user_id}: {e}')

    await rate_limiter.send_message(send)


async def start_timer(context: ContextTypes.DEFAULT_TYPE):
    """Функция, которая будет вызвана через 5 секунд."""
    logging.info("Таймер сработал! Выполняем задачу.")

async def ptb_post_init(app: Application):
    """Функция для первоначальной инициализации приложения."""
    logging.info('Запуск функции post_init.')
    app.job_queue.run_once(
        start_timer,
        when=5,  # Начало через 5 секунд
        context=None,  # Можно передать данные контекста
        name='start_timer',
        misfire_grace_time=None  # Задача не будет пропущена из-за прошлого времени
    )
