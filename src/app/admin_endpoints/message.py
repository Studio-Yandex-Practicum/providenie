import uuid
from datetime import datetime
from pathlib import Path as PathDir
from typing import List, Optional, Union

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
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin_endpoints.constants import (
    EXTRA_PAGE,
    FIRST_PAGE,
    PAGE,
    PAGE_GE,
    PAGE_SIZE,
    PAGE_SIZE_GE,
    PAGE_SIZE_LE,
    STATIC_DIR,
)
from app.core.auth import get_current_admin
from app.core.db import get_async_session
from app.crud.group import crud_group
from app.crud.message import crud_message
from app.crud.photo import crud_photo
from app.crud.user_tg import crud_user
from app.schemas.message import MessageCreate, MessageUpdate
from app.schemas.photo import PhotoCreate

# from bot.services import bot_application

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get(
    '/admin/messages',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
async def messages(
    request: Request,
    is_send: Optional[bool] = Query(None),
    sended_at: Optional[datetime] = Query(None),
    create_user: Optional[int] = Query(None),
    update_users: Optional[int] = Query(None),
    page: int = Query(PAGE, ge=PAGE_GE),
    page_size: int = Query(PAGE_SIZE, ge=PAGE_SIZE_GE, le=PAGE_SIZE_LE),
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
    start_index = (page - FIRST_PAGE) * page_size
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
            + (EXTRA_PAGE if total_messages % page_size > 0 else 0),
        },
    )


@router.get(
    '/admin/messages/create',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
async def get_create_message_form(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Render form for creating a new message."""
    groups = await crud_group.get_all_objs(session=session)
    return templates.TemplateResponse(
        'create_message.html',
        {'request': request, 'groups': groups},
    )


@router.post(
    '/admin/messages/create',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
async def create_messages(
    request: Request,
    text: Optional[str] = Form(None),
    photos: List[UploadFile] = File(...),
    group_id: Optional[List[Union[int, str]]] = Form(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to create a new message."""
    message = MessageCreate(
        text=text,
        create_user=request.user.id,
        update_users=request.user.id,
        groups=group_id,
    )
    new_message = await crud_message.create(message, session)

    directory = PathDir(STATIC_DIR)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    if photos:
        for file_photo in photos:
            if file_photo.filename:
                extension = file_photo.filename.split('.')[-1]
                unique_filename = f'{uuid.uuid4()}.{extension}'
                file_location = f'{directory}/{unique_filename}'

                async with aiofiles.open(file_location, 'wb') as f:
                    content = await file_photo.read()
                    await f.write(content)

                new_photo = PhotoCreate(
                    filename=file_location,
                    message_id=new_message.id,
                )
                await crud_photo.create(new_photo, session)

    # TODO: Вставить запуск задачи отправки сообщения (по аналогии с кодом
    #  функции `load_unsent_messages`, только сообщение у нас лежит в
    #  `new_message`

    return RedirectResponse(
        url='/admin/messages',
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    '/admin/messages/{message_id}/edit',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
async def get_edit_message_form(
    request: Request,
    message_id: int = Path(...),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Render form for editing a message."""
    message = await crud_message.get_obj_by_id(message_id, session)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message with this ID not found.',
        )

    photos = await crud_photo.get_all_by_attributes(
        {'message_id': message_id},
        session,
    )
    return templates.TemplateResponse(
        'edit_message.html',
        {
            'request': request,
            'message': message,
            'photos': photos,
            'is_message_sent': message.is_send,
        },
    )


@router.post(
    '/admin/messages/{message_id}/update',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
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
            detail='Message with this ID not found.',
        )
    message = MessageUpdate(
        text=text,
        is_send=is_send,
        update_users=request.user.id,
        sended_at=sended_at,
    )
    updated_message = await crud_message.update(
        existing_message,
        message,
        session,
    )
    if new_photos:
        directory = PathDir(STATIC_DIR)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        for file_photo in new_photos:
            if file_photo.filename:
                extension = file_photo.filename.split('.')[-1]
                unique_filename = f'{uuid.uuid4()}.{extension}'
                file_location = f'{directory}/{unique_filename}'

                async with aiofiles.open(file_location, 'wb') as f:
                    content = await file_photo.read()
                    await f.write(content)

                new_photo = PhotoCreate(
                    filename=file_location,
                    message_id=updated_message.id,
                )
                await crud_photo.create(new_photo, session)

        photos = await crud_photo.get_all_by_attributes(
            filters={'message_id': message_id},
            session=session,
        )

    # TODO: Вставить запуск задачи отправки сообщения (по аналогии с кодом
    #  функции `load_unsent_messages`, только сообщение у нас лежит в
    #  `updated_message`. Предварительно нужно удалить соответствующую задачу.

    return templates.TemplateResponse(
        'edit_message.html',
        {
            'request': request,
            'message': updated_message,
            'photos': photos,
        },
    )


@router.post(
    '/admin/messages/{message_id}/delete',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
async def delete_message(
    request: Request,
    message_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to delete a message."""
    existing_photos = await crud_photo.get_all_by_attributes(
        filters={'message_id': message_id},
        session=session,
    )
    existing_message = await crud_message.get_obj_by_id(
        obj_id=message_id,
        session=session,
    )
    if not existing_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message with this ID not found.',
        )
    if not existing_photos:
        await crud_message.delete(existing_message, session)
    else:
        for photo in existing_photos:
            await crud_photo.delete(photo, session)
        await crud_message.delete(existing_message, session)

    # TODO: Вставить удаление задачи отправки сообщения. ID сообщения лежит
    #  в `message_id`

    return RedirectResponse(
        url='/admin/messages',
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post(
    '/admin/messages/{message_id}/photos/{photo_id}/delete',
    dependencies=[Depends(get_current_admin)],
    response_class=HTMLResponse,
)
async def delete_photo_from_message(
    request: Request,
    message_id: int,
    photo_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint for delete photo from message."""
    existing_message = await crud_message.get_obj_by_id(message_id, session)
    existing_photo = await crud_photo.get_obj_by_id(
        obj_id=photo_id,
        session=session,
    )
    if not existing_message or not existing_photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Message or photo with this ID not found.',
        )
    await crud_photo.delete(existing_photo, session)
    photos = await crud_photo.get_all_by_attributes(
        filters={'message_id': message_id},
        session=session,
    )
    return templates.TemplateResponse(
        'edit_message.html',
        {'request': request, 'message': existing_message, 'photos': photos},
    )
