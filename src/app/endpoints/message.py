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
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.message import crud_message

router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')


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


@router.get('/admin/messages/{message_id}/edit', response_class=HTMLResponse)
async def get_create_message_form(request: Request) -> HTMLResponse:
    """Render form for creating a new message."""
    return templates.TemplateResponse(
        'edit_message.html',
        {'request': request},
    )
