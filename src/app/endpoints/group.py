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
from app.core.dependencies import get_current_admin
from app.crud.group import crud_group
from app.models import UserTG
from app.schemas.group import GroupCreate, GroupUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/groups', response_class=HTMLResponse)
async def groups(
    request: Request,
    is_active: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> Jinja2Templates:
    """Endpoint to get groups."""
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active

    groups = await crud_group.get_all_by_attributes(filters, session)

    return templates.TemplateResponse(
        'groups.html',
        {'request': request, 'groups': groups})


@router.post('/groups', response_class=HTMLResponse)
async def create_groups(
    request: Request,
    group: GroupCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> HTMLResponse:
    """Endpoint to create a new group."""
    is_unique = await crud_group.get_one_by_attributes(
        {'name': group.name}, session)
    if not is_unique:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Group with this name already exists.')
    new_group = await crud_group.create(group, session)
    return templates.TemplateResponse(
        'group_created.html', {'request': request, 'group': new_group})


@router.patch('/groups/{group_id}', response_class=HTMLResponse)
async def update_group(
    request: Request,
    group: GroupUpdate,
    group_id: int = Path(..., title='Group id in DB'),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> HTMLResponse:
    """Endpoint to update an existing group."""
    existing_group = await crud_group.get_one_by_attributes(
        {'id': group_id}, session)
    if not existing_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group not found.')
    updated_group = await crud_group.update(
        existing_group, group, session)
    return templates.TemplateResponse(
        'group_updated.html',
        {'request': request, 'group': updated_group})
