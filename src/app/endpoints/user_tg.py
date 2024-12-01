from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.db import get_async_session
from app.models.models import Group, UserTG

router = APIRouter()
templates = Jinja2Templates(directory='app/endpoints/templates')


@router.get('/admin/users', response_class=HTMLResponse)
async def admin_users(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    group_id: Optional[int] = None,
) -> HTMLResponse:
    """Retrieve users for admin, with optional group filtering."""
    query = select(UserTG).options(selectinload(UserTG.groups))

    if group_id:
        query = query.join(Group.users).filter(Group.id == group_id)

    result = await session.execute(query)
    users = result.scalars().all()
    groups = await session.execute(
        select(Group),
    )
    groups = groups.scalars().all()

    return templates.TemplateResponse(
        'admin_users.html',
        {
            'request': request,
            'users': users,
            'groups': groups,
            'title': 'Users',
        },
    )


@router.get('/admin/users/{user_id}/edit', response_class=HTMLResponse)
async def edit_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Edit user information."""
    async with session.begin():
        user = await session.get(UserTG, user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        result = await session.execute(select(Group))
        groups = result.scalars().all()

    return templates.TemplateResponse(
        'edit_user.html',
        {
            'request': request,
            'user': user,
            'groups': groups,
            'title': 'Edit User',
        },
    )
