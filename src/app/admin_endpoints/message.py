from datetime import datetime
from pathlib import Path as path_dir
from typing import List, Optional

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.message import crud_message
from app.crud.photo import crud_photo
from app.crud.user_tg import crud_user
from app.schemas.message import MessageCreate, MessageUpdate
from app.schemas.photo import PhotoCreate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


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

    users = await crud_user.get_all_objs(session=session)
    messages = await crud_message.get_all_by_attributes(filters, session)
    messages = sorted(messages, key=lambda message: message.id)
    total_messages = len(messages)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_messages = messages[start_index:end_index]
    return templates.TemplateResponse(
        'admin_messages.html',
        {
            'request': request,
            'users': users,
            'messages': paginated_messages,
            'page': page,
            'total_pages': (total_messages // page_size)
            + (1 if total_messages % page_size > 0 else 0),
        },
    )


@router.get('/admin/messages/create', response_class=HTMLResponse)
async def get_create_message_form(
    request: Request,
    session: AsyncSession = Depends(get_async_session)) -> HTMLResponse:
    """Render form for creating a new message."""
    return templates.TemplateResponse(
        'create_message.html',
        {'request': request},
    )


@router.post('/admin/messages/create', response_class=HTMLResponse)
async def create_messages(
    request: Request,
    text: Optional[str] = Form(None),
    file_photos: List[UploadFile] = File(None),
    session: AsyncSession = Depends(get_async_session),
    ) -> HTMLResponse:
    """Endpoint to create a new message."""
    message = MessageCreate(
        text=text,
        create_user=1,  # TODO Брать из current_user (Depends)
        update_users=1)  # TODO Брать из current_user (Depends)
    new_message = await crud_message.create(message, session)

    directory = path_dir('app/admin_endpoints/static')
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    created_photos = []
    if file_photos:
        for file_photo in file_photos:
            file_location = f"{directory}/{file_photo.filename}"
            async with aiofiles.open(file_location, 'wb') as f:
                content = await file_photo.read()
                await f.write(content)
            new_photo = PhotoCreate(
                filename=file_location, message_id=new_message.id)
            created_photo = await crud_photo.create(new_photo, session)
            created_photos.append(created_photo)
    return templates.TemplateResponse(
        'message_created.html',
        {'request': request, 'message': new_message, 'photo': created_photos})


@router.get('/admin/messages/{message_id}/edit', response_class=HTMLResponse)
async def get_edit_message_form(
    request: Request,
    message_id: int = Path(...),
    session: AsyncSession = Depends(get_async_session)) -> HTMLResponse:
    """Render form for editing a message."""
    message = await crud_message.get_obj_by_id(message_id, session)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message not found.')

    photos = await crud_photo.get_all_by_attributes(
        {'message_id': message_id}, session)
    return templates.TemplateResponse(
        'edit_message.html',
        {
            'request': request,
            'message': message,
            'photos': photos,
            'is_message_sent': message.is_send,
        })


@router.post('/admin/messages/{message_id}/update',
              response_class=HTMLResponse)
async def edit_message(
    request: Request,
    text: Optional[str] = Form(None),
    is_send: Optional[bool] = Form(None),
    sended_at: Optional[datetime] = Form(None),
    message_id: int = Path(..., title='Message id in DB'),
    new_photos: List[UploadFile] = File(None),
    session: AsyncSession = Depends(get_async_session),
    ) -> HTMLResponse:
    """Endpoint to edit an existing message."""
    existing_message = await crud_message.get_obj_by_id(message_id, session)
    if not existing_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message not found.')
    message = MessageUpdate(
        text=text,
        is_send=is_send,
        update_users=1,  # TODO Брать из current_user (Depends)
        sended_at=sended_at)
    updated_message = await crud_message.update(
        existing_message, message, session)
    if new_photos:
        directory = path_dir('app/admin_endpoints/static')
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        created_photos = []
        for file_photo in new_photos:
            if file_photo:
                file_location = f"{directory}/{file_photo.filename}"
                async with aiofiles.open(file_location, 'wb') as f:
                    content = await file_photo.read()
                    await f.write(content)
                new_photo = PhotoCreate(
                    filename=file_location,
                    message_id=updated_message.id)
                created_photo = await crud_photo.create(new_photo, session)
                created_photos.append(created_photo)
    return templates.TemplateResponse(
        'edit_message.html',
        {'request': request,
         'message': updated_message,
         'photos': created_photos,
        })


@router.post('/admin/messages/{message_id}/delete', response_class=HTMLResponse)
async def delete_message(
    request: Request,
    message_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to delete a message."""
    existing_message = await crud_message.get_obj_by_id(message_id, session)
    if not existing_message:
        raise HTTPException(
            status_code=404,
            detail="Message with this ID not found")

    await crud_message.delete(existing_message, session)
    return templates.TemplateResponse(
        'message_deleted.html',
        {'request': request, 'message': existing_message})
