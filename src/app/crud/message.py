from typing import TypeVar

from app.crud.base import CRUDBase
from app.models.models import (Group, Message, MessageGroupAssociation,
                               MessageStatus)
from app.schemas.message import MessageCreate

from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar('ModelType')


class CRUDMessage(CRUDBase):
    """CRUD class for messages."""

    async def create(
        self,
        pydantic_scheme_message: MessageCreate,
        session: AsyncSession,
    ) -> ModelType:
        """Create new user in database."""
        new_message_dict = pydantic_scheme_message.dict()
        groups = new_message_dict.pop('groups', None)
        new_message: Message = self.model(**new_message_dict)
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)

        if groups:
            result = await session.execute(
                select(Group).filter(
                    Group.id.in_(pydantic_scheme_message.groups),
                ),
            )
            group_objects = result.unique().scalars().all()

            for group in group_objects:
                association = MessageGroupAssociation(
                    message_id=new_message.id,
                    group_id=group.id,
                )
                session.add(association)

            await session.commit()

        return new_message

    async def get_unsent_messages(self, session: AsyncSession) -> ModelType:
        """Get unsent messages."""
        unsent_messages = await session.execute(
            select(Message).where(not_(Message.is_send)),
        )

        return unsent_messages.unique().scalars().all()

    async def get_message_statuses(self, session: AsyncSession, message_id: int):
        """Get statuses."""
        statuses = await session.execute(
            select(MessageStatus).where(MessageStatus.message_id == message_id)
        )
        return {s.user_id: s for s in statuses.scalars().all()}


crud_message = CRUDMessage(Message)
