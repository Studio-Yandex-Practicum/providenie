from typing import List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar('ModelType')


class CRUDBase:
    """The base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]) -> None:
        """Initilisation method for CRUDBase class."""
        self.model = model

    async def _get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
        single: bool = False) -> Optional[ModelType]:
        """Get objects by attribute name and attribute value."""
        attr = getattr(self.model, attr_name)
        query = select(self.model).where(attr == attr_value)
        result = await session.execute(query)
        if single:
            result = result.scalars().first()
        else:
            result = result.scalars().all()
        return result

    async def get_one_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession) -> Optional[ModelType]:
        """Get one object by attribute name and attribute value."""
        return await self._get_by_attribute(
            attr_name, attr_value, session, single=True)

    async def get_all_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession) -> List[ModelType]:
        """Get all objects by attribute name and attribute value."""
        return await self._get_by_attribute(
            attr_name, attr_value, session, single=False)

    async def get_obj_by_id(
            self,
            obj_id: int,
            session: AsyncSession) -> Optional[ModelType]:
        """Get one object for object value."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id))
        return db_obj.scalars().first()

    async def get_all_objs(
            self,
            session: AsyncSession) -> List[ModelType]:
        """Get all objects for model."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            pydantic_scheme_obj,
            session: AsyncSession) -> ModelType:
        """Create object in database."""
        db_obj = self.model(**pydantic_scheme_obj.dict())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            pydantic_scheme_obj,
            session: AsyncSession) -> ModelType:
        """Update object in database."""
        obj_data = jsonable_encoder(db_obj)
        update_data = pydantic_scheme_obj.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
