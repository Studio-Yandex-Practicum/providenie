from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.photo import crud_photo

router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')


@router.get('/admin/photos', response_class=HTMLResponse)
async def photos(
    request: Request,
    message_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to get photos."""
    filters = {}
    if message_id is not None:
        filters['message_id'] = message_id

    photos = await crud_photo.get_all_by_attributes(filters, session)

    return templates.TemplateResponse(
        'photos.html',
        {'request': request, 'photos': photos},
    )
