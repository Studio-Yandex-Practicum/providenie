import asyncio
import logging
from datetime import datetime, timedelta

from telegram import InputMediaPhoto
from telegram.ext import Application, ContextTypes

from app.core.db import get_async_session
from app.crud.message import crud_message


async def load_unsent_messages(context: ContextTypes.DEFAULT_TYPE)->None:
    """Загрузка неотправленных сообщений из базы данных.

    Планирование их отправки.
    """
    async with get_async_session() as session:
        unsent_messages = await crud_message.get_unsent_messages(session)
        for message in unsent_messages:
            if message.is_send:
                continue
            if message.send_on < datetime.now():
                send_time = datetime.now() + timedelta(seconds=10)
            else:
                send_time = message.send_on

            context.job_queue.run_once(
                send_message,
                when=send_time,
                data={'message_id': message.id},
                name=f'send_mes_{message.id}',
                )


async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка сообщения пользователям."""
    message_id = context.job.data['message_id']

    async with get_async_session() as session:
        message = await crud_message.get(session, message_id)

    if not message:
        return

    groups = message.groups
    for group in groups:
        for user in group.users:
            if not user.is_active:
                continue
            user_id = user.tg_id
            try:
                if not message.photos:
                    await context.bot.send_message(chat_id=user_id,
                                                   text=message.text)
                elif len(message.photos) == 1:
                    await context.bot.send_photo(chat_id=user_id,
                                                 photo=message.photos[0].filename,
                                                 caption=message.text)
                else:
                    media = [InputMediaPhoto(media=message.photos[i].filename)
                             for i in range(min(10, len(message.photos)))]
                    await context.bot.send_media_group(chat_id=user_id,
                                                       media=media)
                await asyncio.sleep(1 / 20)
            except Exception as e:
                logging.error(f'Ошибка отправки сообщения'
                              f'для пользователя {user_id}: {e}')
                if 'blocked' in str(e):
                    user.is_active = False
                    session.add(user)
                continue

    message.is_send = True
    message.sended_at = datetime.now()
    session.add(message)
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
