import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.user_tg import crud_user
from app.models import UserTG

security = HTTPBasic()


async def get_current_admin(
        credentials: HTTPBasicCredentials = Depends(security),
        session: AsyncSession = Depends(get_async_session)) -> UserTG:
    """Get the current admin user based on tg_id and password."""
    filters = {'tg_id': credentials.username}
    user = await crud_user.get_one_by_attributes(filters, session)
    if user is None or not bcrypt.checkpw(
        credentials.password.encode('utf-8'),
        user.hashed_password.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail='Invalid tg_id or password')
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='You do not have access to this resource')
    return user
