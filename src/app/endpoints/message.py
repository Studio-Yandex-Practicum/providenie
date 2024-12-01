from datetime import datetime
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.message import crud_message
from app.models import UserTG
from app.models.models import UserTG
from app.schemas.message import MessageCreate, MessageUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')


async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
) -> UserTG:
    """Получает текущего пользователя (пример на основе `user_id`)."""
    # Здесь можно заменить на JWT или куки с токеном
    user_id = 1  # Этот ID нужно заменить на получаемый из токена

    user = await session.get(UserTG, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не авторизован',
        )
    return user


@router.get('/admin/messages', response_class=HTMLResponse)
async def messages(
    request: Request,
    is_send: Optional[bool] = Query(None),
    sended_at: Optional[datetime] = Query(None),
    create_user: Optional[int] = Query(None),
    update_users: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to get messages."""
    filters = {}
    if is_send is not None:
        filters['is_send'] = is_send
    if sended_at is not None:
        filters['sended_at'] = sended_at
    if create_user is not None:
        filters['create_user'] = create_user
    if update_users is not None:
        filters['update_users'] = update_users

    messages = await crud_message.get_all_by_attributes(filters, session)

    return templates.TemplateResponse(
        'admin_messages.html',
        {'request': request, 'messages': messages},
    )


@router.get('/admin/messages/create', response_class=HTMLResponse)
async def get_create_message_form(request: Request) -> HTMLResponse:
    """Render form for creating a new message."""
    return templates.TemplateResponse(
        'create_message.html',
        {'request': request},
    )


@router.post('/admin/messages/create', response_class=HTMLResponse)
async def create_messages(
    request: Request,
    text: Optional[str] = Form(...),  # Изменено на Form для обработки формы
    current_user: UserTG = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to create a new message."""
    message_data = MessageCreate(
        text=text,
        create_user=current_user.id,
        update_users=current_user.id,
    )
    new_message = await crud_message.create(message_data, session)
    return templates.TemplateResponse(
        'create_message.html',
        {'request': request, 'message': new_message},
    )


@router.patch('/admin/messages/{message_id}/edit', response_class=HTMLResponse)
async def update_message(
    request: Request,
    text: Optional[str] = Query(None),
    is_send: Optional[bool] = Query(None),
    sended_at: Optional[datetime] = Query(None),
    message_id: int = Path(..., title='Message id in DB'),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to update an existing message."""
    existing_message = await crud_message.get_obj_by_id(message_id, session)
    if not existing_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message not found.',
        )
    message = MessageUpdate(
        text=text,
        is_send=is_send,
        update_users=request.user.id,  # TODO Брать из current_user (Depends)
        sended_at=sended_at,
    )
    updated_message = await crud_message.update(
        existing_message,
        message,
        session,
    )
    return templates.TemplateResponse(
        'message_updated.html',
        {'request': request, 'message': updated_message},
    )
