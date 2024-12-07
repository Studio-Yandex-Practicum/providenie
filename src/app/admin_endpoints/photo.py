from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_admin
from app.core.db import get_async_session
from app.crud.photo import crud_photo
from app.schemas.photo import PhotoCreate, PhotoUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/admin/photos',
             dependencies=[Depends(get_current_admin)],
             response_class=HTMLResponse)
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


@router.post('/admin/photos/create',
              dependencies=[Depends(get_current_admin)],
              response_class=HTMLResponse)
async def create_photo(
    request: Request,
    file: UploadFile = File(...),
    message_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to create a new photo."""
    directory = Path('app/static')
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    file_location = f"{directory}/{file.filename}"
    async with aiofiles.open(file_location, 'wb') as f:
        content = await file.read()
        await f.write(content)
    new_photo = PhotoCreate(filename=file_location, message_id=message_id)
    created_photo = await crud_photo.create(new_photo, session)
    return templates.TemplateResponse(
        'photo_created.html',
        {'request': request, 'photo': created_photo})


@router.post('/admin/photos/{photo_id}/edit',
              dependencies=[Depends(get_current_admin)],
              response_class=HTMLResponse)
async def update_photo(
    request: Request,
    photo_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to edit an existing photo."""
    existing_photo = await crud_photo.get_obj_by_id(photo_id, session)
    if not existing_photo:
        raise HTTPException(
            status_code=404,
            detail="Photo with this ID not found")
    file_location = f"app/static/{file.filename}"
    async with aiofiles.open(file_location, "wb") as f:
        content = await file.read()
        await f.write(content)
    new_photo = PhotoUpdate(filename=file_location)
    updated_photo = await crud_photo.update(existing_photo, new_photo, session)
    return templates.TemplateResponse(
        'photo_updated.html',
        {'request': request, 'photo': updated_photo})


@router.post('/admin/photos/{photo_id}/delete',
              dependencies=[Depends(get_current_admin)],
              response_class=HTMLResponse)
async def delete_photo(
    request: Request,
    photo_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to delete a photo."""
    existing_photo = await crud_photo.get_obj_by_id(photo_id, session)
    if not existing_photo:
        raise HTTPException(
            status_code=404,
            detail="Photo with this ID not found")

    await crud_photo.delete(existing_photo, session)
    return templates.TemplateResponse(
        'photo_deleted.html',
        {'request': request, 'photo_id': photo_id})
