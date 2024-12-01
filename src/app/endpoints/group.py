from typing import Optional

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
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.group import crud_group
from app.schemas.group import GroupCreate, GroupUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')


@router.get('/admin/groups', response_class=HTMLResponse)
async def groups(
    request: Request,
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to get groups with pagination."""
    filters = {}
    if is_active is not None:
        filters['is_active'] = is_active

    groups = await crud_group.get_all_by_attributes(filters, session)

    # Сортировка по id
    groups = sorted(groups, key=lambda group: group.id)

    # Реализация пагинации
    total_groups = len(groups)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_groups = groups[start_index:end_index]

    return templates.TemplateResponse(
        'admin_groups.html',
        {
            'request': request,
            'groups': paginated_groups,
            'page': page,
            'total_pages': (total_groups // page_size)
            + (1 if total_groups % page_size > 0 else 0),
        },
    )


@router.get('/admin/groups/create', response_class=HTMLResponse)
async def create_group_form(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Форма для создания новой группы."""
    return templates.TemplateResponse(
        'create_group.html',
        {'request': request, 'title': 'Create Group'},
    )


@router.post('/admin/groups/create', response_class=HTMLResponse)
async def create_groups(
    request: Request,
    name: str = Form(...),
    is_active: Optional[bool] = Form(True),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to create a new group."""
    existing_group = await crud_group.get_one_by_attributes(
        {'name': name},
        session,
    )
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Group with this name already exists.',
        )
    group = GroupCreate(name=name, is_active=is_active)
    new_group = await crud_group.create(group, session)
    return templates.TemplateResponse(
        'create_group.html',
        {'request': request, 'group': new_group},
    )


@router.get('/admin/groups/{group_id}/edit', response_class=HTMLResponse)
async def get_group_edit_page(
    request: Request,
    group_id: int = Path(..., title='Group id in DB'),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Эндпоинт для отображения страницы редактирования группы."""
    existing_group = await crud_group.get_one_by_attributes(
        {'id': group_id},
        session,
    )
    if not existing_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Группа не найдена.',
        )
    return templates.TemplateResponse(
        'edit_group.html',
        {'request': request, 'group': existing_group},
    )


@router.post('/admin/groups/{group_id}/edit', response_class=HTMLResponse)
async def update_group(
    request: Request,
    name: str = Form(...),
    is_active: Optional[bool] = Form(True),
    group_id: int = Path(..., title='Group id in DB'),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Эндпоинт для обновления группы."""
    method = await request.form()
    if method.get('_method') == 'patch':  # Checking if it's a PATCH request
        existing_group = await crud_group.get_one_by_attributes(
            {'id': group_id},
            session,
        )
        if not existing_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Группа не найдена.',
            )
        group = GroupUpdate(name=name, is_active=is_active)
        updated_group = await crud_group.update(existing_group, group, session)
        return templates.TemplateResponse(
            'edit_group.html',
            {'request': request, 'group': updated_group},
        )
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
