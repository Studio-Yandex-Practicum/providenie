from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.models import (
    Group,
    Message,
    Photo,
    UserTG,
)
from app.schemas import (
    GroupBase,
    MessageEdit,
    MessageOut,
    PhotoOut,
    UserCreate,
    UserOut,
    UserTGBaseWithGroup,
)

app = FastAPI(debug=True)
router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')
app.mount(
    '/static',
    StaticFiles(directory='app/endpoints/static'),
    name='static',
)


# Эндпоинт для получения всех пользователей с возможностью фильтрации по группе
@router.get('/users/', response_model=List[UserTGBaseWithGroup])
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    group_id: Optional[int] = None,
):
    """Получить всех пользователей, с возможностью фильтрации по группе."""
    query = select(UserTG)
    if group_id:
        query = query.join(Group.users).filter(Group.id == group_id)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


# Эндпоинт для создания нового пользователя
@router.post('/users/', response_model=UserOut)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать нового пользователя."""
    new_user = UserTG(
        tg_id=user_data.tg_id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_name=user_data.user_name,
        is_admin=user_data.is_admin,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


# Эндпоинт для редактирования данных пользователя
@router.put('/users/{user_id}', response_model=UserOut)
async def update_user(
    user_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    user_name: Optional[str] = None,
    is_admin: Optional[bool] = None,
    tg_id: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session),
):
    """Редактировать данные пользователя (кроме группы и пароля)."""
    user = await session.get(UserTG, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    # Обновляем только переданные параметры
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if user_name is not None:
        user.user_name = user_name
    if is_admin is not None:
        user.is_admin = is_admin
    if tg_id is not None:
        user.tg_id = tg_id

    await session.commit()
    await session.refresh(user)
    return user


# Эндпоинт для получения всех сообщений
@router.get('/messages/', response_model=List[MessageOut])
async def get_messages(
    session: AsyncSession = Depends(get_async_session),
    status: str = 'all',
):
    """Получить сообщения: все, отправленные или ожидающие."""
    query = select(Message).order_by(
        Message.send_on.desc(),
    )  # Сортировка по дате отправки
    if status == 'sent':
        query = query.filter(Message.is_send)
    elif status == 'pending':
        query = query.filter(~Message.is_send)
    result = await session.execute(query)
    messages = result.scalars().all()
    return messages


# Эндпоинт для создания нового сообщения с фотографиями
@router.post('/messages/', response_model=dict)
async def create_message(
    text: str,
    photos: Optional[List[str]] = None,
    create_user: int = 1,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новое сообщение с фотографиями."""
    new_message = Message(
        text=text,
        create_user=create_user,
        update_users=create_user,
    )
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)

    if photos:
        photo_objects = [
            Photo(filename=photo, message_id=new_message.id)
            for photo in photos
        ]
        session.add_all(photo_objects)
        await session.commit()

    return {
        'message': 'Message created',
        'message_id': new_message.id,
    }


# Эндпоинт для редактирования сообщения
@router.put('/messages/{message_id}', response_model=dict)
async def edit_message(
    message_id: int,
    message_data: MessageEdit,
    session: AsyncSession = Depends(get_async_session),
):
    """Редактировать сообщение, если оно не отправлено."""
    message = await session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail='Message not found')

    if message.is_send:
        raise HTTPException(status_code=400, detail='Cannot edit sent message')

    if message_data.text:
        message.text = message_data.text

    if message_data.photos:
        # Удаляем старые фотографии
        await session.execute(
            update(Photo)
            .where(Photo.message_id == message_id)
            .delete(synchronize_session='fetch'),
        )
        photo_objects = [
            Photo(filename=photo, message_id=message.id)
            for photo in message_data.photos
        ]
        session.add_all(photo_objects)

    await session.commit()
    return {'message': 'Message updated successfully'}


# Эндпоинт для получения списка групп
@router.get('/groups/', response_model=List[GroupBase])
async def get_groups(session: AsyncSession = Depends(get_async_session)):
    """Получить список групп."""
    result = await session.execute(select(Group))
    groups = result.scalars().all()
    return groups


# Эндпоинт для получения фотографий сообщения
@router.get('/messages/{message_id}/photos/', response_model=List[PhotoOut])
async def get_message_photos(
    message_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получить фотографии для сообщения."""
    result = await session.execute(
        select(Photo).filter(Photo.message_id == message_id),
    )
    photos = result.scalars().all()
    return photos
