from typing import TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.endpoints.validators import check_tg_id_unique
from app.models.models import UserTG

ModelType = TypeVar('ModelType')


class CRUDUserTG(CRUDBase):
    """CRUD class for users."""

    async def create(
            self,
            pydantic_scheme_user: ModelType,
            session: AsyncSession) -> ModelType:
        """Create new user in database."""
        new_user_dict = pydantic_scheme_user.dict()
        await check_tg_id_unique(pydantic_scheme_user, session)
        password = new_user_dict.pop('password')
        new_user_dict['hashed_password'] = hash(password)
        new_user = self.model(**new_user_dict)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def update(
            self,
            db_user: ModelType,
            pydantic_scheme_user: ModelType,
            session: AsyncSession) -> ModelType:
        """Update user in database."""
        user_data = jsonable_encoder(db_user)
        update_data = pydantic_scheme_user.dict(
            exclude_unset=True,
            exclude_none=True)
        if 'tg_id' in update_data:
            await check_tg_id_unique(pydantic_scheme_user, session)
        if 'password' in update_data:
            password = update_data.pop('password')
            update_data['hashed_password'] = hash(password)
        for field in update_data:
            if hasattr(user_data, field):
                setattr(db_user, field, update_data[field])
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


crud_user = CRUDUserTG(UserTG)
