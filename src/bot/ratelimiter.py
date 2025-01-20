import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from telegram import InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes

from app.core.db import get_async_session_context
from app.crud.message import crud_message
from app.crud.user_tg import crud_user
from app.schemas.message import MessageUpdate


async def load_unsent_messages(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Загрузка неотправленных сообщений из базы данных.

    Планирование их отправки.
    """
    async with get_async_session_context() as session:
        unsent_messages = await crud_message.get_unsent_messages(session)
        for message in unsent_messages:
            # Преобразование строки времени в datetime
            if message.send_on < datetime.now():
                send_time = timedelta(minutes=1)  # Delay 1 minutes
            else:
                send_time = message.send_on - datetime.now()

            # Передаём message_id и user_id в данные задачи
            job = context.job_queue.run_once(
                send_message,
                when=send_time,
                data={
                    'message_id': message.id,
                    'user_id': message.create_user,  # Передаём ID пользователя
                },
                name=f'send_mes_{message.id}',
                job_kwargs={
                    'misfire_grace_time': None,
                },
            )
            logging.info(f'Запланирована задача {job.name} на {job.next_t}')


async def send_message_to_user(
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    message: Any,
) -> None:
    """Отправляет сообщение пользователю по его ID."""
    if not message.photos:
        await context.bot.send_message(
            chat_id=user_id,
            text=message.text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif len(message.photos) == 1:
        await context.bot.send_photo(
            chat_id=user_id,
            parse_mode=ParseMode.MARKDOWN,
            photo=message.photos[0].filename,
            caption=message.text,
        )
    else:
        media = [
            InputMediaPhoto(
                media=open(message.photos[i].filename, 'rb'),  # noqa: ASYNC230
            )
            for i in range(min(10, len(message.photos)))
        ]
        await context.bot.send_media_group(
            chat_id=user_id,
            parse_mode=ParseMode.MARKDOWN,
            media=media,
            caption=message.text,
        )
    await asyncio.sleep(1 / 20)


async def send_message(context: ContextTypes.DEFAULT_TYPE) -> None:  # noqa: C901
    """Отправка сообщения пользователям."""
    message_id = context.job.data['message_id']
    user_id = context.job.data.get('user_id')  # Извлекаем ID пользователя

    async with get_async_session_context() as session:
        message = await crud_message.get_obj_by_id(
            obj_id=message_id,
            session=session,
        )

        if not message:
            return  # Если сообщение не найдено, выходим из функции

        groups = message.groups
        if groups:
            # Если у сообщения есть группы,
            # отправляем сообщения пользователям из групп
            # Если пользователь состоит оновременно в нескольких группах,
            # то в сете он все равно окажется в единственном экземпляре.
            users_to_notify = {
                user.tg_id
                for group in groups
                for user in group.users
                if user.is_active
            }

            for user_id in users_to_notify:
                await send_message_to_user(context, user_id, message)
        else:
            # Если групп нет, получаем всех активных пользователей,
            # исключая администратора и заблокированных
            active_users = await crud_user.get_all_by_attributes(
                filters={
                    'is_admin': False,
                },
                session=session,
            )

            for user in active_users:
                if user.is_active and not user.is_block:
                    await send_message_to_user(context, user.tg_id, message)

        # Обновление статуса сообщения через CRUD-функцию
        await crud_message.update(
            db_obj=message,
            pydantic_scheme_obj=MessageUpdate(
                is_send=True,
                sended_at=datetime.now(),
                update_users=user_id,
            ),
            session=session,
        )


async def ptb_post_init(app: Application) -> None:
    """Функция для первоначальной инициализации приложения."""
    logging.info('Запуск функции post_init.')
    app.job_queue.run_once(
        load_unsent_messages,
        when=5,
        data=None,
        name='load_unsent_messages',
        job_kwargs={
            'misfire_grace_time': None,
        },
    )
