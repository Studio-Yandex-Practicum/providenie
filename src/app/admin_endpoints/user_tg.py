from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.group import crud_group
from app.crud.user_tg import crud_user
from app.models.models import Group
from app.schemas.user_tg import UserCreate, UserUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/admin/users', response_class=HTMLResponse)
async def get_users(
    request: Request,
    group_id: Optional[int] = Query(None),
    is_admin: Optional[bool] = Query(None),
    is_block: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    ) -> HTMLResponse:
    """Endpoint to get users."""
    filters = {}
    if group_id is not None:
        filters['group_id'] = group_id
    if is_admin is not None:
        filters['is_admin'] = is_admin
    if is_block is not None:
        filters['is_block'] = is_block
    users = await crud_user.get_users_by_params(filters, session)
    users = sorted(users, key=lambda user: user.id)
    groups = await crud_group.get_all_objs(session)
    total_users = len(users)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_users = users[start_index:end_index]
    return templates.TemplateResponse(
        'admin_users.html',
        {'request': request,
         'users': paginated_users,
            'page': page,
            'total_pages': (total_users // page_size)
            + (1 if total_users % page_size > 0 else 0),
         'groups': groups})


@router.get('/admin/users/create', response_class=HTMLResponse)
async def create_users(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    )-> HTMLResponse:
    """Endpoint to get form a new user."""
    groups = await crud_group.get_all_objs(session)
    return templates.TemplateResponse(
        'create_user.html', {'request': request, 'groups': groups})


@router.post('/admin/users/create', response_class=HTMLResponse)
async def create_users(
    request: Request,
    tg_id: str = Form(...),
    first_name: str = Form(...),
    last_name: Optional[str] = Form(None),
    user_name: Optional[str] = Form(None),
    is_block: Optional[bool] = Form(False),
    is_admin: Optional[bool] = Form(False),
    password: Optional[str] = Form(None),
    is_active: Optional[bool] = Query(True),
    group_id: Optional[List[int]] = Form(None), # Переименовал из groups в group_id под шаблон  # noqa: E501
    session: AsyncSession = Depends(get_async_session),
    )-> HTMLResponse:
    """Endpoint to create a new user."""
    user = UserCreate(
        tg_id=tg_id,
        first_name=first_name,
        last_name=last_name,
        user_name=user_name,
        is_block=is_block,
        is_admin=is_admin,
        password=password,
        is_active=is_active,
        groups=group_id) # Переименовал из groups в group_id под шаблон
    user = await crud_user.create(user, session)
    groups = await session.execute(select(Group).filter(
                Group.id.in_(group_id))) # Переименовал из groups в group_id под шаблон  # noqa: E501
    groups = groups.scalars().all()
    return templates.TemplateResponse(
        'user_created.html', {'request': request,
                              'user': user,
                              'groups': groups})


@router.get('/admin/users/{user_id}/edit', response_class=HTMLResponse)
async def get_user_edit_form(
    request: Request,
    user_id: int = Path(..., title='The ID of the user to update'),
    is_block: Optional[bool] = Form(False),
    is_admin: Optional[bool] = Form(False),
    password: Optional[str] = Form(None),
    group_id: Optional[List[int]] = Query(None), # Переименовал из groups в group_id под шаблон  # noqa: E501
    session: AsyncSession = Depends(get_async_session),
    ) -> HTMLResponse:
    """Endpoint to get editing form an existing user."""
    existing_user = await crud_user.get_one_by_attributes(
        {'id': user_id}, session)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.')
    user = UserUpdate(
        id=user_id,
        is_block=is_block,
        is_admin=is_admin,
        password=password,
        groups=group_id)  # Переименовал из groups в group_id под шаблон
    groups = await crud_group.get_all_objs(session)
    return templates.TemplateResponse(
        'edit_user.html', {'request': request,
                              'user': user,
                              'groups': groups})


@router.post('/admin/users/{user_id}/edit', response_class=HTMLResponse)
async def edit_user(
    request: Request,
    user_id: int = Path(..., title='The ID of the user to update'),
    is_block: Optional[bool] = Form(False),
    is_admin: Optional[bool] = Form(False),
    password: Optional[str] = Form(None),
    group_id: Optional[List[int]] = Form(None), # Переименовал из groups в group_id под шаблон  # noqa: E501
    session: AsyncSession = Depends(get_async_session),
    ) -> HTMLResponse:
    """Endpoint to update an existing user."""
    existing_user = await crud_user.get_one_by_attributes(
        {'id': user_id}, session)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.')
    user_scheme = UserUpdate(
        id=user_id,
        is_block=is_block,
        is_admin=is_admin,
        password=password,
        groups=group_id) # Переименовал из groups в group_id под шаблон
    updated_user = await crud_user.update(existing_user, user_scheme, session)
    if group_id:  # Переименовал из groups в group_id под шаблон
        groups = await session.execute(select(Group).filter(
                    Group.id.in_(user_scheme.groups)))
        groups = groups.scalars().all()
    return templates.TemplateResponse(
        'user_updated.html', {'request': request,
                              'user': updated_user,
                              'groups': groups})
