from typing import TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
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
        password = new_user_dict.pop('password')
        # TODO: "заменить на получение хеша после создания функций для
        # авторизации"
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
        if 'password' in update_data:
            password = update_data.pop('password')
            # TODO: "заменить на получение хеша после создания функций
            # для авторизации"
            update_data['hashed_password'] = hash(password)
        for field in update_data:
            if hasattr(user_data, field):
                setattr(db_user, field, update_data[field])
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def check_tg_id_unique(
            self,
            pydantic_scheme_user: ModelType,
            session: AsyncSession) -> bool:
        """Check unique telegram id for new user.

        Returns True if there is no user with such a tg_id and False otherwise.
        """
        tg_id = pydantic_scheme_user.tg_id
        user_exists = await session.execute(
            select(exists().where(UserTG.tg_id == tg_id)))
        return not user_exists.scalar()


crud_user = CRUDUserTG(UserTG)
