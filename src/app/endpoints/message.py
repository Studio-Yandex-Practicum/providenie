from datetime import datetime
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Query,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.message import crud_message
from app.models.models import Photo

router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')


@router.get('/admin/messages', response_class=HTMLResponse)
async def messages(
    request: Request,
    is_send: Optional[bool] = Query(None),
    sended_at: Optional[datetime] = Query(None),
    create_user: Optional[int] = Query(None),
    update_users: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
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
    total_messages = len(messages)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_messages = messages[start_index:end_index]
    return templates.TemplateResponse(
        'admin_messages.html',
        {
            'request': request,
            'messages': paginated_messages,
            'page': page,
            'total_pages': (total_messages // page_size)
            + (1 if total_messages % page_size > 0 else 0),
        },
    )


@router.get('/admin/messages/create', response_class=HTMLResponse)
async def get_create_message_form(request: Request) -> HTMLResponse:
    """Render form for creating a new message."""
    return templates.TemplateResponse(
        'create_message.html',
        {'request': request},
    )


@router.get('/admin/messages/{message_id}/edit', response_class=HTMLResponse)
async def edit_message(
    request: Request,
    message_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Get a message by its ID for editing, along with associated photos."""
    # Fetch the message by its ID
    message = await crud_message.get_obj_by_id(message_id, session)

    # Fetch the photos related to the message
    result = await session.execute(
        select(Photo).filter(Photo.message_id == message_id),
    )
    photos = result.scalars().all()

    return templates.TemplateResponse(
        'edit_message.html',
        {
            'request': request,
            'message': message,
            'photos': photos,
            'is_message_sent': message.is_send,
        },
    )
