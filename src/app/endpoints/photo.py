from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.photo import crud_photo
from app.schemas.photo import PhotoCreate, PhotoUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


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
        {'request': request, 'photos': photos})


@router.post('/admin/photos/create', response_class=HTMLResponse)
async def create_photo(
    request: Request,
    filename: str = Query(...),
    message_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to create a new photo."""
    file_location = f"staticfiles/{filename}"
   # async with aiofiles.open(file_location, "wb") as f:
    #     content = await filename.read()
    #     await f.write(content) TODO Исправить после того как станет ясно
    #                             откуда брать и куда сохранять фото.
    new_photo = PhotoCreate(filename=file_location, message_id=message_id)
    created_photo = await crud_photo.create(new_photo, session)
    return templates.TemplateResponse(
        'photo_created.html',
        {'request': request, 'photo': created_photo})


@router.patch('/admin/photos/{photo_id}/edit', response_class=HTMLResponse)
async def update_photo(
    request: Request,
    photo_id: int,
    filename: str = Query(...),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to update an existing photo."""
    existing_photo = await crud_photo.get_obj_by_id(photo_id, session)
    if not existing_photo:
        raise HTTPException(
            status_code=404,
            detail="Photo with this ID not found")
    file_location = f"staticfiles/{filename}"
    # async with aiofiles.open(file_location, "wb") as f:
    #     content = await filename.read()
    #     await f.write(content) TODO Исправить после того как станет ясно
    #                             откуда брать и куда сохранять фото.
    new_photo = PhotoUpdate(filename=file_location)
    updated_photo = await crud_photo.update(existing_photo, new_photo, session)
    return templates.TemplateResponse(
        'photo_updated.html',
        {'request': request, 'photo': updated_photo})
