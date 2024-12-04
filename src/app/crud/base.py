from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar('ModelType')


class CRUDBase:
    """The base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]) -> None:
        """Initialialising method for CRUDBase class."""
        self.model = model

    async def _get_by_attributes(
        self,
        filters: Dict[str, Any],
        session: AsyncSession,
        single: bool = False) -> Optional[ModelType]:
        """Get objects by multiple attributes."""
        conditions = []
        for attr, value in filters.items():
            condition = getattr(self.model, attr) == value
            conditions.append(condition)
        query = select(self.model).where(and_(*conditions))
        result = await session.execute(query)
        if single:
            result = result.scalars().first()
        else:
            result = result.scalars().all()
        return result

    async def get_one_by_attributes(
        self,
        filters: Dict[str, Any],
        session: AsyncSession) -> Optional[ModelType]:
        """Get one object by multiple attributes."""
        return await self._get_by_attributes(filters, session, single=True)

    async def get_all_by_attributes(
        self,
        filters: Dict[str, Any],
        session: AsyncSession) -> List[ModelType]:
        """Get all objects by multiple attributes."""
        return await self._get_by_attributes(filters, session, single=False)

    async def get_obj_by_id(
            self,
            obj_id: int,
            session: AsyncSession) -> Optional[ModelType]:
        """Get one object by object id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id))
        return db_obj.scalars().first()

    async def get_all_objs(
            self,
            session: AsyncSession) -> List[ModelType]:
        """Get all objects by model."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            pydantic_scheme_obj: ModelType,
            session: AsyncSession) -> ModelType:
        """Create object in database."""
        db_obj = self.model(**pydantic_scheme_obj.dict())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            pydantic_scheme_obj: ModelType,
            session: AsyncSession) -> ModelType:
        """Update object in database."""
        update_data = pydantic_scheme_obj.dict(
            exclude_unset=True,
            exclude_none=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
