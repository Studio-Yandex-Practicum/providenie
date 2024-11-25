from typing import Optional

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.dependencies import get_current_admin
from app.crud.photo import crud_photo
from app.models import UserTG
from app.schemas.photo import PhotoCreate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/photos', response_class=HTMLResponse)
async def photos(
    request: Request,
    message_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> Jinja2Templates:
    """Endpoint to get photos."""
    filters = {}
    if message_id is not None:
        filters['message_id'] = message_id

    photos = await crud_photo.get_all_by_attributes(filters, session)

    return templates.TemplateResponse(
        'photos.html',
        {'request': request, 'photos': photos})


@router.post('/photos', response_class=HTMLResponse)
async def create_photo(
    request: Request,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    message_id: int = Field(...)) -> HTMLResponse:
    """Endpoint to create a new photo."""
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    new_photo = PhotoCreate(filename=file.filename, message_id=message_id)
    created_photo = await crud_photo.create(new_photo, session)
    return templates.TemplateResponse(
        'photo_created.html',
        {'request': request, 'photo': created_photo})
