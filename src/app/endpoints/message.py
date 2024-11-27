from datetime import datetime
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
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
from app.schemas.message import MessageCreate, MessageUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


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
        'messages.html',
        {'request': request, 'messages': messages})


@router.post('/admin/messages/create', response_class=HTMLResponse)
async def create_messages(
    request: Request,
    text: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_async_session),
    ) -> HTMLResponse:
    """Endpoint to create a new message."""
    message = MessageCreate(
        text=text,
        create_user=request.user.id,  # TODO Брать из current_user (Depends)
        update_users=request.user.id)  # TODO Брать из current_user (Depends)
    new_message = await crud_message.create(message, session)
    return templates.TemplateResponse(
        'message_created.html',
        {'request': request, 'message': new_message})


@router.patch('/admin/messages/{message_id}/edit',
              response_class=HTMLResponse)
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
            detail='Message not found.')
    message = MessageUpdate(
        text=text,
        is_send=is_send,
        update_users=request.user.id,  # TODO Брать из current_user (Depends)
        sended_at=sended_at)
    updated_message = await crud_message.update(
        existing_message, message, session)
    return templates.TemplateResponse(
        'message_updated.html',
        {'request': request, 'message': updated_message})
