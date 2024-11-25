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

from src.app.core.db import get_async_session
from src.app.core.dependencies import get_current_admin
from src.app.crud.user_tg import crud_user
from src.app.models import UserTG
from src.app.schemas.user_tg import UserCreate, UserUpdate

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/users', response_class=HTMLResponse)
async def get_users(
    request: Request,
    groups: Optional[str] = Query(None),
    is_admin: Optional[bool] = Query(None),
    is_blocked: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> Jinja2Templates:
    """Endpoint to get users."""
    filters = {}
    if groups is not None:
        filters['groups'] = groups
    if is_admin is not None:
        filters['is_admin'] = is_admin
    if is_blocked is not None:
        filters['is_blocked'] = is_blocked

    users = await crud_user.get_all_by_attributes(filters, session)

    return templates.TemplateResponse(
        'users.html',
        {'request': request, 'users': users})


@router.post('/users', response_class=HTMLResponse)
async def create_users(
    request: Request,
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> HTMLResponse:
    """Endpoint to create a new user."""
    is_unique = await crud_user.check_tg_id_unique(user, session)
    if not is_unique:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this tg_id already exists.')
    new_user = await crud_user.create(user, session)
    return templates.TemplateResponse(
        'user_created.html', {'request': request, 'user': new_user})


@router.patch('/users/{tg_id}', response_class=HTMLResponse)
async def update_user(
    request: Request,
    user: UserUpdate,
    tg_id: int = Path(..., title='The Telegram ID of the user to update'),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserTG = Depends(get_current_admin)) -> HTMLResponse:
    """Endpoint to update an existing user."""
    existing_user = await crud_user.get_one_by_attributes(
        {'tg_id': tg_id}, session)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.")
    updated_user = await crud_user.update(tg_id, user, session)
    return templates.TemplateResponse(
        'user_updated.html', {'request': request, 'user': updated_user})
