from typing import TypeVar

from sqlalchemy import delete, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.core.jwt import get_hash_password
from app.crud.base import CRUDBase
from app.models.models import Group, UserGroupAssociation, UserTG

ModelType = TypeVar('ModelType')


class CRUDUserTG(CRUDBase):
    """CRUD class for users."""

    async def create(
        self,
        pydantic_scheme_user: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Create new user in database."""
        new_user_dict = pydantic_scheme_user.dict()
        password = new_user_dict.pop('password')
        groups = new_user_dict.pop('groups')
        new_user_dict['hashed_password'] = get_hash_password(password)
        new_user: UserTG = self.model(**new_user_dict)
        session.add(new_user)
        if groups:
            result = await session.execute(select(Group).filter(
                Group.id.in_(pydantic_scheme_user.groups)))
            group_objects = result.scalars().all()

        for group in group_objects:
            association = UserGroupAssociation(
                user_id=new_user.id, group_id=group.id)
            session.add(association)

        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def update(
        self,
        db_user: ModelType,
        pydantic_scheme_user: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Update user in database."""
        update_data = pydantic_scheme_user.dict(
            exclude_unset=True,
            exclude_none=True)
        if 'password' in update_data:
            password = update_data.pop('password')
            update_data['hashed_password'] = get_hash_password(password)

        if 'groups' in update_data:
            groups = update_data.pop('groups')
            await session.execute(
                delete(UserGroupAssociation).filter(
                    UserGroupAssociation.user_id == db_user.id))
            for group_id in groups:
                association = UserGroupAssociation(
                    user_id=db_user.id, group_id=group_id)
                session.add(association)
        for field, value in update_data.items():
           if hasattr(db_user, field):
               setattr(db_user, field, value)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def check_tg_id_unique(
        self,
        pydantic_scheme_user: ModelType,
        session: AsyncSession,
    ) -> bool:
        """Check unique telegram id for new user.

        Returns True if there is no user with such a tg_id and False otherwise.
        """
        tg_id = pydantic_scheme_user.tg_id
        user_exists = await session.execute(
            select(exists().where(UserTG.tg_id == tg_id)),
        )
        return not user_exists.scalar()

    async def get_users_by_params(
            self,
            filters: dict,
            session: AsyncSession) -> ModelType:
        """Get user by params."""
        query = select(UserTG).options(joinedload(UserTG.groups))
        conditions = []
        if 'group_id' in filters and filters['group_id'] is not None:
            conditions.append(UserTG.groups.any(
                Group.id == filters['group_id']))
        if 'is_admin' in filters:
            conditions.append(UserTG.is_admin == filters['is_admin'])
        if 'is_block' in filters:
            conditions.append(UserTG.is_block == filters['is_block'])
        if conditions:
            query = query.where(*conditions)
        result = await session.execute(query)
        return result.unique().scalars().all()


crud_user = CRUDUserTG(UserTG)
