from typing import List, Optional, Union

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
)
from app.core.auth import get_current_admin
from app.core.db import get_async_session
from app.crud.group import crud_group
from app.crud.user_tg import crud_user
from app.schemas.user_tg import UserCreate, UserUpdate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/admin/users",
            dependencies=[Depends(get_current_admin)],
            response_class=HTMLResponse)
async def get_users(
    request: Request,
    group_id: Optional[Union[int, str]] = Query(None),
    is_admin: Optional[Union[bool, str]] = Query(None),
    is_block: Optional[Union[bool, str]] = Query(None),
    page: int = Query(PAGE, ge=PAGE_GE),
    page_size: int = Query(PAGE_SIZE, ge=PAGE_SIZE_GE, le=PAGE_SIZE_LE),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to get users."""
    filters = {}
    if isinstance(group_id, int):
        filters["group_id"] = group_id
    if isinstance(is_admin, bool):
        filters["is_admin"] = is_admin
    if isinstance(is_block, bool):
        filters["is_block"] = is_block
    users = await crud_user.get_users_by_params(filters, session)
    users = sorted(users, key=lambda user: user.id)
    groups = await crud_group.get_all_objs(session)
    total_users = len(users)
    start_index = (page - FIRST_PAGE) * page_size
    end_index = start_index + page_size
    paginated_users = users[start_index:end_index]
    return templates.TemplateResponse(
        "admin_users.html",
        {
            "request": request,
            "users": paginated_users,
            "page": page,
            "total_pages": (total_users // page_size)
            + (EXTRA_PAGE if total_users % page_size > 0 else 0),
            "groups": groups,
        },
    )


@router.get("/admin/users/create",
            dependencies=[Depends(get_current_admin)],
            response_class=HTMLResponse)
async def create_users(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to get form a new user."""
    groups = await crud_group.get_all_objs(session)
    return templates.TemplateResponse(
        "create_user.html", {"request": request, "groups": groups},
    )


@router.post("/admin/users/create",
             dependencies=[Depends(get_current_admin)],
             response_class=HTMLResponse)
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
    group_id: Optional[List[Union[int, str]]] = Form(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to create a new user."""
    existing_user = await crud_user.get_one_by_attributes(
        {"tg_id": tg_id},
        session,
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this Telegram ID already exists.",
        )
    user_data = {
    "tg_id": tg_id,
    "first_name": first_name,
    "last_name": last_name,
    "user_name": user_name,
    "is_block": is_block,
    "is_admin": is_admin,
    "password": password,
    "is_active": is_active,
    "groups": group_id}

    if not user_data["password"]:
        user = UserCreate(**user_data)
        user_copy = user.copy(exclude={"password"})
    else:
        user_copy = UserCreate(**user_data)
    user = await crud_user.create(user_copy, session)
    return RedirectResponse(url="/admin/users",
                            status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin/users/{user_id}/edit",
            dependencies=[Depends(get_current_admin)],
            response_class=HTMLResponse)
async def get_user_edit_form(
    request: Request,
    user_id: int = Path(..., title="The ID of the user to update"),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to get editing form an existing user."""
    existing_user = await crud_user.get_one_by_attributes(
        {"id": user_id}, session)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with this ID is not found.')
    groups = await crud_group.get_all_objs(session)
    user = await crud_user.get_user_with_groups(existing_user, session)
    return templates.TemplateResponse(
        "edit_user.html",
        {"request": request, "user": user, "groups": groups})


@router.post("/admin/users/{user_id}/edit",
             dependencies=[Depends(get_current_admin)],
             response_class=HTMLResponse)
async def edit_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user to update"),
    is_block: Optional[bool] = Form(False),
    is_admin: Optional[bool] = Form(False),
    password: Optional[str] = Form(None),
    group_id: Optional[List[Union[int, str]]] = Form(None),
    session: AsyncSession = Depends(get_async_session),
) -> HTMLResponse:
    """Endpoint to update an existing user."""
    existing_user = await crud_user.get_one_by_attributes(
        {"id": user_id}, session)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with this ID is not found.')
    user_scheme = UserUpdate(
        id=user_id,
        is_block=is_block,
        is_admin=is_admin,
        password=password,
        groups=group_id)
    await crud_user.update(existing_user, user_scheme, session)
    return RedirectResponse(
        url="/admin/users/", status_code=status.HTTP_303_SEE_OTHER)
