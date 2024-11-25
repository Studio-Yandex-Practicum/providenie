from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.dependencies import get_current_admin
from app.crud.message import crud_message
from app.models import UserTG
from app.schemas.message import MessageCreate, MessageUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/messages', response_class=HTMLResponse)
async def messages(
    request: Request,
    is_send: bool,
    sended_at: DateTime,
    create_user: int,
    update_users: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> Jinja2Templates:
    """Endpoint to get messages."""
    filters = {}
    if is_send is not None:
        filters['is_send'] = is_send
    if sended_at is not None:
        filters['sended_at'] = sended_at
    if create_user is not None:
        filters['create_user'] = create_user
    if update_users is not None:
        update_users['update_users'] = update_users

    messages = await crud_message.get_all_by_attributes(filters, session)

    return templates.TemplateResponse(
        'messages.html',
        {'request': request, 'messages': messages})


@router.post('/messages', response_class=HTMLResponse)
async def create_messages(
    request: Request,
    message: MessageCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> HTMLResponse:
    """Endpoint to create a new message."""
    new_message = await crud_message.create(message, session)
    return templates.TemplateResponse(
        'message_created.html', {'request': request, 'message': new_message})


@router.patch('/messages/{message_id}', response_class=HTMLResponse)
async def update_message(
    request: Request,
    message: MessageUpdate,
    message_id: int = Path(..., title='Message id in DB'),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> HTMLResponse:
    """Endpoint to update an existing message."""
    existing_message = await crud_message.get_one_by_attributes(
        {'id': message_id}, session)
    if not existing_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message not found.')
    updated_message = await crud_message.update(
        existing_message, message, session)
    return templates.TemplateResponse(
        'message_updated.html',
        {'request': request, 'message': updated_message})
