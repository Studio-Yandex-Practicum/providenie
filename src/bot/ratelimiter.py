import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from telegram import InputMediaPhoto
from telegram.ext import Application, ContextTypes

from app.core.db import get_async_session
from app.crud.message import crud_message
from app.crud.user_tg import crud_user


async def load_unsent_messages(context: ContextTypes.DEFAULT_TYPE)->None:
    """Загрузка неотправленных сообщений из базы данных.

    Планирование их отправки.
    """
    async with get_async_session() as session:
        unsent_messages = await crud_message.get_unsent_messages(session)
        for message in unsent_messages:
            # Преобразование строки времени в datetime
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


async def send_message_to_user(context: ContextTypes.DEFAULT_TYPE,
                               user_id: int, message: Any)-> None:
    """Отправляет сообщение пользователю по его ID."""
    if not message.photos:
        await context.bot.send_message(chat_id=user_id, text=message.text)
    elif len(message.photos) == 1:
        await context.bot.send_photo(chat_id=user_id,
                                                 photo=message.photos[0].filename,
                                                 caption=message.text)
    else:
        media = [InputMediaPhoto(media=message.photos[i].filename)
                             for i in range(min(10, len(message.photos)))]
        await context.bot.send_media_group(chat_id=user_id, media=media)
    await asyncio.sleep(1 / 20)


async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка сообщения пользователям."""
    message_id = context.job.data['message_id']

    async with get_async_session() as session:
        message = await crud_message.get(session, message_id)

    if not message:
        return  # Если сообщение не найдено, выходим из функции

    groups = message.groups
    if groups:
        # Если у сообщения есть группы,
        # отправляем сообщения пользователям из групп
        for group in groups:
            for user in group.users:
                if user.is_active:  # Убедитесь, что пользователь активен
                    await send_message_to_user(context, user.tg_id, message)
    else:
        # Если групп нет, получаем всех активных пользователей,
        # исключая администратора и заблокированных
        async with get_async_session() as session:
            query = crud_user.get_all_active_users_excluding_admin_and_blocked(
                session)
            active_users = await query

        for user in active_users:
            await send_message_to_user(context, user.tg_id, message)

    # Обновление статуса сообщения после отправки
    message.is_send = True
    message.sended_at = datetime.now()
    async with get_async_session() as session:
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
