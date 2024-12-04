import asyncio
import logging
import os
from collections import deque
from datetime import datetime, timedelta
from typing import Any, Callable

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from telegram import Bot
from telegram.ext import Application, ApplicationBuilder, ContextTypes

from app.models.models import Message

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
job_queue = application.job_queue


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


async def load_unsent_messages(context: ContextTypes.DEFAULT_TYPE)->None:
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
                if message.send_on < datetime.now():
                    send_time = datetime.now() + timedelta(seconds=10)
                else:
                    send_time = message.send_on

                job_queue.run_once(
                    send_message,
                    when=send_time.timestamp(),
                    context={"message_id": message.id},
                    name=f'send_mes_{message.id}',
                    )


async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка сообщения пользователям."""
    message_id = context.job.data

    async with SessionLocal() as session:
        message = await session.get(Message, message_id)
        if not message:
            return
        groups = message.groups
        for group in groups:
            user_ids = [user.tg_id for user in group.users]
            for user_id in user_ids:
                if message.photos:
                    await bot.send_photo(chat_id=user_id, photo=message.photos,
                                         caption=message.text)
                else:
                    await bot.send_message(chat_id=user_id, text=message.text)
                await asyncio.sleep(1/20)

        message.is_send = True
        message.sended_at = datetime.now()
        await session.commit()


async def ptb_post_init(app: Application)-> None:
    """Функция для первоначальной инициализации приложения."""
    logging.info('Запуск функции post_init.')
    app.job_queue.run_once(
        load_unsent_messages,
        when=5,
        context=None,
        name='load_unsent_messages',
        misfire_grace_time=None,
    )
